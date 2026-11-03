import copy
import pickle

import pynmea2
import pytest


SENTENCES = (
    '$PSRF100,0,1200,8,1,1',
    '$PSRF156,1',
    '$PTNL,PJT,NAD83(Conus),CaliforniaZone 4 0404',
    '$PTNLDG,44.0,33.0,287.0,100,0,4,1,0,,,',
    '$PLCJ,5F01,66FC,AA,9390,6373',
    '$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,',
    '$PGRME,15.0,M,45.0,M,25.0,M*1C',
    '$PUBX,04,073824.00,131014,113903.99,1814,16,495176,342.504,21*18',
    '$PASHR,LTN,3*3D',
    '$PFEC,GPatt,294.7,-02.5,+00.4*45',
    '$PNORBT4,1.234,-1.234,1.234,23.4,12.34567,12.3*3D',
    '$PRDID,-1.31,7.81,47.31*68',
    '$PSXN,23,0.30,-0.97,298.57,0.13*1B',
    '$PVTX,0002,181330,00005.22,M,262.518,T,-01.967,09.358,W*7E',
    '$PMGNST,02.12,3,T,534,05.0,+03327,00*40',
    '$PKWDWPL,053125,V,4531.7900,N,12253.4800,W,,,200320,,AC7FD-1,/-*10',
    ('$PKNDS,114400,A,4954.1450,N,11923.6043,W,001.4,356.8,'
     '130223,19.20,W00,U00002,207,00,*2E'),
    '$PKNSH,4954.1450,N,11923.6043,W,114400,A,U00002,*44',
    ('$PKLDS,122434,A,4954.1474,N,11923.6044,W,001.1,194.9,'
     '130223,19.20,W00,100,1001,80,00,*60'),
    '$PKLSH,4954.1474,N,11923.6044,W,122434,A,100,1001,*3F',
    '$PANZ,,RSI,65,0.0,6.7,S,0',
)
PROTOCOLS = range(pickle.HIGHEST_PROTOCOL + 1)


@pytest.mark.parametrize('sentence', SENTENCES)
@pytest.mark.parametrize('protocol', PROTOCOLS)
def test_pickle_roundtrip(sentence, protocol):
    msg = pynmea2.parse(sentence)
    msg.note = {'kept': ['saved state']}
    msg.data_alias = msg.data
    restored = pickle.loads(pickle.dumps(msg, protocol))
    assert type(restored) is type(msg)
    assert restored.__dict__ == msg.__dict__
    assert restored.data_alias is restored.data
    assert restored.data is not msg.data
    assert restored.render() == msg.render()


@pytest.mark.parametrize('protocol', PROTOCOLS)
def test_pickle_preserves_class_after_dispatch_data_changes(protocol):
    msg = pynmea2.parse('$PSRF100,0,1200,8,1,1')
    msg.data[0] = 'unregistered'
    restored = pickle.loads(pickle.dumps(msg, protocol))
    assert type(restored) is type(msg)
    assert restored.data == msg.data
    assert restored.render() == msg.render()


@pytest.mark.parametrize('protocol', PROTOCOLS)
def test_pickle_preserves_shared_references_and_cycles(protocol):
    msg = pynmea2.parse('$PSRF156,1')
    msg.self_reference = msg
    restored, shared_data = pickle.loads(
        pickle.dumps((msg, msg.data), protocol))
    assert restored.self_reference is restored
    assert restored.data is shared_data
    assert restored.data == msg.data


@pytest.mark.parametrize('deep', (False, True))
def test_copy_preserves_type_and_data_ownership(deep):
    msg = pynmea2.parse('$PSRF156,1')
    msg.data_alias = msg.data
    restored = copy.deepcopy(msg) if deep else copy.copy(msg)
    assert type(restored) is type(msg)
    assert restored is not msg
    assert restored.__dict__ == msg.__dict__
    assert restored.data_alias is restored.data
    assert (restored.data is msg.data) is (not deep)


@pytest.mark.parametrize('sentence', SENTENCES)
def test_normal_constructor_still_requires_arguments(sentence):
    cls = type(pynmea2.parse(sentence))
    with pytest.raises(TypeError):
        cls()


class SlotSentence(pynmea2.ProprietarySentence):
    __slots__ = ('extra',)


class SlotSiRF(pynmea2.srf.SRF100):
    __slots__ = ('extra',)


class HookSentence(pynmea2.ProprietarySentence):
    def __getstate__(self):
        state = dict(self.__dict__)
        state.pop('transient', None)
        return {'saved_dict': state}

    def __setstate__(self, state):
        self.__dict__.update(state['saved_dict'])
        self.restored_via_hook = True


class HookSiRF(HookSentence, pynmea2.srf.SRF100):
    pass


@pytest.mark.parametrize('cls', (SlotSentence, SlotSiRF))
@pytest.mark.parametrize('protocol', range(2, pickle.HIGHEST_PROTOCOL + 1))
def test_pickle_preserves_slots(cls, protocol):
    msg = object.__new__(cls)
    cls.__init__(msg, 'SRF', ['100', '0', '1200', '8', '1', '1'])
    assert type(msg) is cls
    msg.extra = 'slot metadata'
    restored = pickle.loads(pickle.dumps(msg, protocol))
    assert type(restored) is cls
    assert restored.extra == 'slot metadata'
    assert restored.__dict__ == msg.__dict__


@pytest.mark.parametrize('cls', (HookSentence, HookSiRF))
@pytest.mark.parametrize('protocol', PROTOCOLS)
def test_pickle_honors_custom_state_hooks(cls, protocol):
    msg = object.__new__(cls)
    cls.__init__(msg, 'SRF', ['100', '0', '1200', '8', '1', '1'])
    assert type(msg) is cls
    msg.transient = 'must not persist'
    restored = pickle.loads(pickle.dumps(msg, protocol))
    assert type(restored) is cls
    assert restored.data == msg.data
    assert restored.restored_via_hook is True
    assert not hasattr(restored, 'transient')


class CustomNewSentence(pynmea2.ProprietarySentence):
    def __new__(cls, manufacturer, data, token):
        result = object.__new__(cls)
        result.allocated_token = token
        return result

    def __init__(self, manufacturer, data, token):
        super(CustomNewSentence, self).__init__(manufacturer, data)

    def __getnewargs__(self):
        return self.manufacturer, self.data, self.allocated_token

    def __getstate__(self):
        return {'manufacturer': self.manufacturer, 'data': self.data}


@pytest.mark.parametrize('protocol', range(2, pickle.HIGHEST_PROTOCOL + 1))
def test_pickle_honors_subclass_allocation_arguments(protocol):
    msg = CustomNewSentence('ZZZ', ['payload'], 'from constructor')
    restored = pickle.loads(pickle.dumps(msg, protocol))
    assert type(restored) is CustomNewSentence
    assert restored.data == msg.data
    assert restored.allocated_token == 'from constructor'


class CustomReductionSentence(pynmea2.srf.SRF100):
    def __new__(cls, *args):
        return object.__new__(cls)

    def __reduce__(self):
        return type(self), ('SRF', ['100', '1', '9600', '7', '1', '0'])


@pytest.mark.parametrize('protocol', PROTOCOLS)
def test_pickle_honors_subclass_reduction(protocol):
    msg = CustomReductionSentence('SRF', ['100', '0', '1200', '8', '1', '1'])
    assert type(msg) is CustomReductionSentence
    restored = pickle.loads(pickle.dumps(msg, protocol))
    assert type(restored) is CustomReductionSentence
    assert restored.baud == '9600'
