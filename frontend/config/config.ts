// config/config.ts

import { defineConfig } from 'umi';
import routes from './routes';

export default defineConfig({
  routes: routes,
  devServer:{
    proxy:{
      '/api':{
        target:"http://localhost:8101",
        changeOrigin: true,  //改变原始主机头为目标 URL
      }
    }
  }
});