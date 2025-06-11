import { GoogleChatBot } from '../googleChatBot';
import OpenAI from 'openai';

jest.mock('openai');

const MockOpenAI = OpenAI as jest.MockedClass<typeof OpenAI>;

describe('GoogleChatBot', () => {
  beforeEach(() => {
    MockOpenAI.mockClear();
  });

  it('returns reply text from OpenAI API', async () => {
    const create = jest.fn().mockResolvedValue({
      choices: [{ message: { content: 'hi' } }],
    });
    MockOpenAI.mockImplementation(() => ({
      chat: { completions: { create } },
    }) as any);
    const bot = new GoogleChatBot();
    const reply = await bot.handleMessage('hello');
    expect(reply).toBe('hi');
  });

  it('handles errors gracefully', async () => {
    const create = jest.fn().mockRejectedValue(new Error('fail'));
    MockOpenAI.mockImplementation(() => ({
      chat: { completions: { create } },
    }) as any);
    const bot = new GoogleChatBot();
    const reply = await bot.handleMessage('hello');
    expect(reply).toBe("Sorry, I couldn't process your request.");
  });
});

