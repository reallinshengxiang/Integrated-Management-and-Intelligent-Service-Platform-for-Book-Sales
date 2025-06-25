import axios from "axios";
import store from "@/store";
import router from "@/router"


console.log(import.meta.env.VITE_APP_BASE_API)

const DEFAULT_HEADER = {
    "Content-Type": 'application/json',
    "Authorization": "",
}

const http = axios.create({
    baseURL:import.meta.env.VITE_APP_BASE_API,
    timeout:10*1000,
    withCredentials:true,
})

http.interceptors.request.use(opt=>{
    DEFAULT_HEADER.Authorization = store.state.token
    Object.assign(opt.headers,DEFAULT_HEADER);
    return opt;
})

http.interceptors.response.use(opt=>{
    if (opt.data.code === -666){
        console.log(store)
        store.dispatch('reset')
        router.go(0)
    }else{
        return opt
    }

})

const createRestfulAPI = (url)=>{
    return {
        get(params, header){
            return http.get(url,{
                params: params,
                headers: header
            })
        },
        post(params, data, header){
            return http.post(url,data,{
                params: params,
                headers: header
            })
        },
        put(params, data, header) {
            return http.put(url,data,{
                params: params,
                headers: header
            })
        },
        delete(params, data, header){
            return http.delete(url,{
                params: params,
                data: data,
                headers: header
            })
        }
    }
}


export const user = createRestfulAPI('/user');

export const author = createRestfulAPI('/author');

export const book = createRestfulAPI('/book');

export const book_copy = createRestfulAPI('/book_copy');

export const borrow = createRestfulAPI('/borrow');

export const auth = {
    login(data){
        return http.post("/auth/login",data,{})
    },
    register(data){
        return http.post("/auth/register",data,{})
    }
}

export const return_bookcopy = (data) => {
    return http.post("/return_book",data,{})
}

export const upload_url = "/api/uploads"
