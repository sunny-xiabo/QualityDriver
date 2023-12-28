declare module '*.svg';
declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';

interface IResult <T>{
    data:T;
    code: number;
    msg: string;
    success:boolean;
    http_code: number;
    trace_id:string;
    headers:Record<string,any>
}