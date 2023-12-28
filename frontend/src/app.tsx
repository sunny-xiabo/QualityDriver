import { RequestConfig } from 'umi';

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