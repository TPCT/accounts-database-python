const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/graduation project',
    createProxyMiddleware({
      target: 'http://localhost',
      changeOrigin: true,
    })
  );
};