import { request } from "umi";

export const login = (data:Login.ILoginParams) => {
    return request<IResult<boolean>>('/user/login',{
        method:'post',
        data,
    })
}
