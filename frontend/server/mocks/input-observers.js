module.exports = function(app) {
  var express = require('express');
  var inputObserversRouter = express.Router();
  inputObserversRouter.get('/', function(req, res) {
    res.send({"input-observers": [
      {
        id: 0,
        zvalue: 1,
        visualization: 'line_segment',
        visualizations: ['line_segment', 'values'],
        properties: {
          color: '#0000ff'
        },
        input: 1,
        value: 0,
        view: 1
      },
      {
        id: 2,
        zvalue: 0,
        visualization: 'image',
        visualizations: ['image'],
        properties: {
          color: '#00ff00'
        },
        input: 2,
        value: 1,
        view: 1
      },
      {
        id: 3,
        zvalue: 0,
        visualization: 'rotated_rectangle',
        visualizations: ['rotated_rectangle', 'value'],
        properties: {
          color: '#ff00ff'
        },
        input: 2,
        value: 4,
        view: 2
      },
      {
        id: 4,
        zvalue: 5,
        visualization: 'point',
        visualizations: ['point', 'value'],
        properties: {
          color: '#ff0000'
        },
        input: 1,
        value: 6,
        view: 1
      }
    ]});
  });
  inputObserversRouter.post('/', function(req, res) {
    res.send({
      "input-observer": { id: 5 }
    });
  });
  inputObserversRouter.put('/', function(req, res) {
    res.send('null');
  });
  inputObserversRouter.delete('/', function(req, res) {
    res.send('null');
  });
  app.use('/api/inputObservers', inputObserversRouter);
  app.use('/api/inputObservers/*', inputObserversRouter);
};
