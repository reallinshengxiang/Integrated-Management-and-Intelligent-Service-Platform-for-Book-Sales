import { createRouter, createWebHashHistory } from "vue-router";
import Home from "../views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import store from "@/store";

const routes = [
  { 
    path: "/", 
    name: "home",
    redirect: "/index/user"
  },
  {
    path: "/index/:type",
    name: "index",
    component: Home,
    props: true
  },
  {
    path: "/auth/:login",
    name: "login",
    component: LoginView,
    props: true
  },
];

const route = createRouter({
  history: createWebHashHistory(),
  routes,
});

route.beforeEach((to, from, next)=>{
  console.log(to)
  if(to.name === 'login' || store.state.token){
    next()
  }else{
    next({name:'login',params:{login:"login"}})
  }

})

export default route
