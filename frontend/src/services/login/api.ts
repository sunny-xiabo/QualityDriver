import { request } from "umi";

export const login = (data:Login.ILoginParams) => {
    return request<IResult<boolean>>('http://127.0.0.1:8101/api/user/login',{
        method:'post',
        data,
    })
}
