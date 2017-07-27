  export default [
  {
    id: 1,
    title: 'Input image',
    operator: 2,
    connection: null,
    observers: [0, 4],
    variant: {
      ident: 'image',
      title: 'Mono image 8-bit'
    },
    behavior: 'persistent',
    currentType: 'input'
  },
  {
    id: 2,
    title: 'Number',
    operator: 1,
    connection: 1,
    observers: [2, 3],
    variant: {
      ident: 'int',
      title: 'Int32'
    },
    behavior: 'persistent',
    currentType: 'input'
  },
  {
    id: 3,
    title: 'Destination image',
    operator: 2,
    connection: 2,
    observers: [],
    variant: {
      ident: 'image',
      title: 'Mono image 8-bit'
    },
    behavior: 'persistent',
    currentType: 'input'
  },
  {
    id: 4,
    title: 'Some input',
    operator: 3,
    connection: null,
    observers: [],
    variant: {
      ident: 'image',
      title: 'Mono image 8-bit'
    },
    behavior: 'persistent',
    currentType: 'input'
  },
  {
    id: 5,
    title: 'Input',
    operator: 6,
    connection: null,
    observers: [],
    variant: {
      ident: 'int',
      title: 'Int32'
    },
    behavior: 'persistent',
    currentType: 'input'
  }
];
