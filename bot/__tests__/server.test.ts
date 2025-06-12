import request from 'supertest';

let MockBot: jest.MockedClass<any>;

beforeEach(() => {
  jest.resetModules();
  jest.mock('../googleChatBot');
  MockBot = require('../googleChatBot').GoogleChatBot;
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

describe('/mcp endpoint', () => {
  it('accepts valid secret', async () => {
    process.env.MCP_SECRET = 's3cr3t';
    MockBot.mockImplementation(() => ({
      handleMessage: jest.fn().mockResolvedValue('pong'),
    }) as any);
    const { app } = require('../index');
    const response = await request(app)
      .post('/mcp')
      .set('X-MCP-Secret', 's3cr3t')
      .send({ text: 'ping' });
    expect(response.status).toBe(200);
    expect(response.body.text).toBe('pong');
  });

  it('rejects invalid secret', async () => {
    process.env.MCP_SECRET = 's3cr3t';
    MockBot.mockImplementation(() => ({
      handleMessage: jest.fn().mockResolvedValue('pong'),
    }) as any);
    const { app } = require('../index');
    const response = await request(app)
      .post('/mcp')
      .set('X-MCP-Secret', 'bad')
      .send({ text: 'ping' });
    expect(response.status).toBe(401);
  });
});
