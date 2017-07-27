export default [
  {
    id: 1,
    title: 'Port',
    variant: {
      ident: 'int',
      title: 'Int32'
    },
    value: 50123,
    minimum: 49152,
    maximum: 65535,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'inactive',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 1,
    observers: []
  },
  {
    id: 2,
    title: 'Data flow',
    variant: {
      ident: 'enum',
      title: 'Enum'
    },
    value: 2,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'none',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [0, 1, 2],
    operator: 2,
    observers: []
  },
  {
    id: 3,
    title: 'Kernel size',
    variant: {
      ident: 'float',
      title: 'Float32'
    },
    value: 2.5,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 2,
    observers: [0]
  },
  {
    id: 4,
    title: 'Coefficient',
    variant: {
      ident: 'float',
      title: 'Float32'
    },
    value: 2.5,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'timedOut',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 2,
    observers: []
  },
  {
    id: 6,
    title: 'Offset',
    variant: {
      ident: 'float',
      title: 'Float32'
    },
    value: 4.5,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 2,
    observers: []
  },
  {
    id: 5,
    title: 'Host',
    variant: {
      ident: 'string',
      title: 'String'
    },
    value: 'localhost',
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'inactive',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 3,
    observers: []
  },
  {
    id: 7,
    title: 'Kernel variant',
    variant: {
      ident: 'enum',
      title: 'Enum'
    },
    value: 4,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'accessFailed',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 2,
    observers: []
  },
  {
    id: 8,
    title: 'Matrix parameter',
    variant: {
      ident: 'matrix',
      title: 'Int Matrix'
    },
    value: {
      rows: 3,
      cols: 4,
      values: [
        [10, 10, 200, 200],
        [10, 20, 200, 300],
        [10, 30, 200, 400]
      ]
    },
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 9,
    title: 'Strange variant',
    variant: {
      ident: 'none',
      title: ''
    },
    value: null,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'inactive',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 10,
    title: 'Trigger',
    variant: {
      ident: 'trigger',
      title: 'Trigger'
    },
    value: null,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 11,
    title: 'False bool property',
    variant: {
      ident: 'bool',
      title: 'Bool'
    },
    value: false,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 12,
    title: 'Kernel variant',
    variant: {
      ident: 'enum',
      title: 'Enum'
    },
    value: 3,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [3, 4, 5],
    operator: 2,
    observers: []
  },
  {
    id: 13,
    title: 'Image',
    variant: {
      ident: 'image',
      title: 'RGB Image'
    },
    value: {
      width: 200,
      height: 300,
      values: null,
    },
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 14,
    title: 'True bool property',
    variant: {
      ident: 'bool',
      title: 'Bool'
    },
    value: true,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 15,
    title: 'Push parameter',
    variant: {
      ident: 'matrix',
      title: '32-bit float matrix'
    },
    value: null,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'accessFailed',
    access: 'full',
    behavior: 'push',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 16,
    title: 'Pull parameter',
    variant: {
      ident: 'float',
      title: 'Float32'
    },
    value: 3.0,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'pull',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 17,
    title: 'File parameter',
    variant: {
      ident: 'file',
      title: 'File'
    },
    value: {
      name: '28e5-8a4c-c5cf-375b.xml',
      content: null
    },
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 4,
    observers: []
  },
  {
    id: 18,
    title: 'Input parameter',
    variant: {
      ident: 'float',
      title: 'Float32'
    },
    value: 42.0,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'persistent',
    currentType: 'parameter',
    originalType: 'input',
    descriptions: [],
    operator: 6,
    observers: []
  },
  {
    id: 19,
    title: 'Output parameter',
    variant: {
      ident: 'float',
      title: 'Float32'
    },
    value: 43.0,
    minimum: 0,
    maximum: 0,
    rows: 0,
    cols: 0,
    state: 'current',
    access: 'full',
    behavior: 'pull',
    currentType: 'parameter',
    originalType: 'output',
    descriptions: [],
    operator: 6,
    observers: []
  },
  {
    id: 20,
    title: 'Null matrix',
    variant: {
      ident: 'matrix',
      title: '32-bit float matrix'
    },
    value: null,
    minimum: 0,
    maximum: 0,
    rows: 2,
    cols: 3,
    state: 'current',
    access: 'full',
    behavior: 'pull',
    currentType: 'parameter',
    originalType: 'parameter',
    descriptions: [],
    operator: 6,
    observers: []
  }
];
