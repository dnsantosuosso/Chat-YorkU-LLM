const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (app) {
  app.use(
    '/api/*',
    createProxyMiddleware({
      target: 'http://127.0.0.1:8000',
    })
  );
  app.use(
    createProxyMiddleware('/websocket/sendMessage', {
      target: 'ws://127.0.0.1:8000',
      ws: true,
    })
  );
};
