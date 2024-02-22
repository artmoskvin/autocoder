import pytest
from autocoder.ai import AI

@pytest.fixture
def ai_instance():
    # Mocking the BaseChatModel for testing
    class MockModel:
        def stream(self, messages):
            yield from ('response chunk ' + str(i) for i in range(3))

    return AI(model=MockModel())

def test_stream(ai_instance):
    messages = ['Test message']
    response_chunks = list(ai_instance.stream(messages))
    assert response_chunks == ['response chunk 0', 'response chunk 1', 'response chunk 2']