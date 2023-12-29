// config/routes.ts

export default [
  { exact: true, path: '/', component: './login' },
  { exact: true, path: '/home', compenent: './home' },
  {
    path: '*',
    redirect: '/',
  },
];
