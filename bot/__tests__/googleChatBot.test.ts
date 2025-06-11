import { GoogleChatBot } from '../googleChatBot';
import { OpenAIApi } from 'openai';

jest.mock('openai');

const MockOpenAIApi = OpenAIApi as jest.MockedClass<typeof OpenAIApi>;

describe('GoogleChatBot', () => {
  beforeEach(() => {
    MockOpenAIApi.mockClear();
    process.env.OPENAI_API_KEY = 'test-key';
  });

  it('returns reply text from OpenAI API', async () => {
    const createChatCompletion = jest.fn().mockResolvedValue({
      data: { choices: [{ message: { content: 'hi' } }] },
    });
    MockOpenAIApi.mockImplementation(() => ({ createChatCompletion } as any));
    const bot = new GoogleChatBot();
    const reply = await bot.handleMessage('hello');
    expect(reply).toBe('hi');
  });

  it('handles errors gracefully', async () => {
    const createChatCompletion = jest.fn().mockRejectedValue(new Error('fail'));
    MockOpenAIApi.mockImplementation(() => ({ createChatCompletion } as any));
    const bot = new GoogleChatBot();
    const reply = await bot.handleMessage('hello');
    expect(reply).toBe("Sorry, I couldn't process your request.");
  });

  it('throws a readable error when API key is missing', () => {
    delete process.env.OPENAI_API_KEY;
    expect(() => new GoogleChatBot()).toThrow(
      'Missing OPENAI_API_KEY. Please set the OPENAI_API_KEY environment variable.'
    );
  });
});

