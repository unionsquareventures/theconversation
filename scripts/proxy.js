var httpProxy = require('http-proxy');
var url = require('url');
var fs = require('fs');

// Open script file
var scriptTags = fs.readFileSync('proxy_script.html');

httpProxy.createServer(function(req, res, proxy) {

  var isHtml = false,
      write = res.write,
      writeHead = res.writeHead,
      params = url.parse(req.url, true).query,
      dest = params.dest || 'localhost',
      destination;

  dest = dest.match(/^http/) ? dest : 'http://' + dest;
  destination = url.parse(dest, true);

  req.headers['host'] = destination.host;
  req.headers['url'] = destination.href;

  delete req.headers['accept-encoding'];

  res.writeHead = function(code, headers) {
    isHtml = headers['content-type'] && headers['content-type'].match('text/html');
    writeHead.apply(this, arguments);
  }

  res.write = function(data, encoding) {
    if (isHtml && params.dest) {
      var str = data.toString();

      var baseTag = '<base href="' + (dest.replace(/\/$/, '') || '') + '"/>';

      str = str.replace(/(<head[^>]*>)/, "$1" + "\n" + scriptTags + "\n" + baseTag);

      data = new Buffer(str);
    }

    write.call(this, data, encoding);
  };

  proxy.proxyRequest(req, res, {
    host: destination.host,
    port: 80,
  });
}).listen(9000, function () {
  console.log("Waiting for requests...");
});