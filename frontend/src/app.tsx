import { RequestConfig } from 'umi';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/home';



export const request: RequestConfig = {
  timeout: 60000,
  errorConfig: {},
  middlewares: [],
  requestInterceptors: [
    (url,options)=>{
        return {
            url: `/api${url}`,
            options
        }
    }
  ],
  responseInterceptors: [],
};


