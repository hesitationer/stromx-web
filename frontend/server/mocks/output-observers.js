module.exports = function(app) {
  var express = require('express');
  var outputObserversRouter = express.Router();
  outputObserversRouter.get('/', function(req, res) {
    res.send({"output-observers": [
      {
        id: 3,
        zvalue: 3,
        visualization: 'value',
        visualizations: ['value'],
        properties: {
          color: '#ff0000'
        },
        output: 4,
        value: 2,
        view: 1
      },
      {
        id: 4,
        zvalue: 4,
        visualization: 'polygon',
        visualizations: ['polygon', 'value'],
        properties: {
          color: '#00ff00'
        },
        output: 5,
        value: 3,
        view: 1
      },
      {
        id: 5,
        zvalue: 4,
        visualization: 'rectangle',
        visualizations: ['rectangle', 'value'],
        properties: {
          color: '#00ffff'
        },
        output: 5,
        value: 5,
        view: 2
      },
      {
        id: 6,
        zvalue: 5,
        visualization: 'polyline',
        visualizations: ['polyline', 'value'],
        properties: {
          color: '#ff0000'
        },
        output: 5,
        value: 6,
        view: 2
      },
      {
        id: 7,
        zvalue: 6,
        visualization: 'value',
        visualizations: ['value'],
        properties: {
          color: '#ff0000'
        },
        output: 5,
        value: 7,
        view: 2
      }
    ]});
  });
  outputObserversRouter.post('/', function(req, res) {
    res.send({
      "output-observer": { id: 8 }
    });
  });
  outputObserversRouter.put('/', function(req, res) {
    res.send('null');
  });
  outputObserversRouter.delete('/', function(req, res) {
    res.send('null');
  });
  app.use('/api/outputObservers', outputObserversRouter);
  app.use('/api/outputObservers/*', outputObserversRouter);
};
