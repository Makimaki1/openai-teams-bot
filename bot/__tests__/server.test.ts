import request from 'supertest';
import { GoogleChatBot } from '../googleChatBot';

jest.mock('../googleChatBot');

const MockBot = GoogleChatBot as jest.MockedClass<typeof GoogleChatBot>;

beforeEach(() => {
  MockBot.mockClear();
});

describe('/chat endpoint', () => {
  it('returns bot response', async () => {
    MockBot.mockImplementation(() => ({
      handleMessage: jest.fn().mockResolvedValue('pong'),
    }) as any);
    const { app } = require('../index');
    const response = await request(app)
      .post('/chat')
      .send({ message: { text: 'ping' } });
    expect(response.status).toBe(200);
    expect(response.body.text).toBe('pong');
  });

  it('returns 400 when message text is missing', async () => {
    const { app } = require('../index');
    const response = await request(app).post('/chat').send({});
    expect(response.status).toBe(400);
    expect(response.body.error).toMatch(/text is required/i);
  });
});

