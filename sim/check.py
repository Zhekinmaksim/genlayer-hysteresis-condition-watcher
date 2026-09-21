import hashlib
import pathlib
import types


class UserError(Exception):
    pass


class Address(str):
    pass


class TreeMap(dict):
    @classmethod
    def __class_getitem__(cls, _item):
        return cls


class DynArray(list):
    @classmethod
    def __class_getitem__(cls, _item):
        return cls


class Keccak256:
    def __init__(self):
        self.value = hashlib.sha3_256()

    def update(self, data):
        self.value.update(data)

    def hexdigest(self):
        return self.value.hexdigest()


class Event:
    def emit(self):
        pass


class Public:
    write = staticmethod(lambda fn: fn)
    view = staticmethod(lambda fn: fn)


class Nondet:
    responses = []
    web = types.SimpleNamespace(render=lambda *_args, **_kwargs: "status")

    @classmethod
    def exec_prompt(cls, _prompt, **_kwargs):
        return cls.responses.pop(0)


class EqPrinciple:
    strict_eq = staticmethod(lambda fn: fn())
    prompt_non_comparative = staticmethod(lambda fn, **_kwargs: fn())


gl = types.SimpleNamespace(
    Contract=object,
    Event=Event,
    public=Public(),
    vm=types.SimpleNamespace(UserError=UserError),
    message=types.SimpleNamespace(sender_address=Address("0xaaa")),
    nondet=Nondet,
    eq_principle=EqPrinciple(),
)
namespace = {
    "Address": Address,
    "TreeMap": TreeMap,
    "DynArray": DynArray,
    "Keccak256": Keccak256,
    "allow_storage": lambda cls: cls,
    "u32": int,
    "u256": int,
    "gl": gl,
}
root = pathlib.Path(__file__).resolve().parents[1]
source = (root / "contract.py").read_text().replace("from genlayer import *", "")
exec(compile(source, str(root / "contract.py"), "exec"), namespace)

clock = {"now": 1_000_000}


def timestamp():
    clock["now"] += 60
    return clock["now"]


namespace["_timestamp"] = timestamp


def fresh(n=3):
    watcher = namespace["Watcher"]()
    watcher.watches = TreeMap()
    watcher.open_watch("case", "service is healthy", "static status", False, n, 60)
    return watcher


def trigger_and_clear():
    watcher = fresh(3)
    Nondet.responses = ["HOLDS", "HOLDS", "HOLDS"]
    for _ in range(3):
        watcher.check("case")
    assert watcher.get_state("case") == namespace["S_TRIGGERED"]
    Nondet.responses = ["CLEAR", "CLEAR", "CLEAR"]
    for _ in range(3):
        watcher.check("case")
    assert watcher.get_state("case") == namespace["S_CLEAR"]


def unknown_preserves_streak():
    watcher = fresh(2)
    Nondet.responses = ["HOLDS", "UNKNOWN", "HOLDS"]
    watcher.check("case")
    watcher.check("case")
    assert watcher.watches["case"].confirm_streak == 1
    watcher.check("case")
    assert watcher.get_state("case") == namespace["S_TRIGGERED"]
    assert watcher.watches["case"].undetermined_checks == 1


def clear_resets_confirmation():
    watcher = fresh(2)
    Nondet.responses = ["HOLDS", "CLEAR"]
    watcher.check("case")
    watcher.check("case")
    assert watcher.watches["case"].confirm_streak == 0


def bounded_history():
    watcher = fresh(1)
    Nondet.responses = ["HOLDS"] * 25
    for _ in range(25):
        watcher.check("case")
    assert len(watcher.watches["case"].last_results) == 20


def interval_guard():
    watcher = fresh(2)
    times = iter([2_000_000, 2_000_001])
    original = namespace["_timestamp"]
    namespace["_timestamp"] = lambda: next(times)
    try:
        Nondet.responses = ["HOLDS"]
        watcher.check("case")
        try:
            watcher.check("case")
        except UserError as exc:
            assert str(exc) == "CHECK_TOO_SOON"
            return
        raise AssertionError("CHECK_TOO_SOON")
    finally:
        namespace["_timestamp"] = original


tests = [
    trigger_and_clear,
    unknown_preserves_streak,
    clear_resets_confirmation,
    bounded_history,
    interval_guard,
]
for test in tests:
    test()
    print("PASS", test.__name__)
print(f"{len(tests)}/{len(tests)} pass")
