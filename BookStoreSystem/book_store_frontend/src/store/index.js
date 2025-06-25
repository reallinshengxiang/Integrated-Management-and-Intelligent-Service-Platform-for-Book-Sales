import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

const state_set = {
  token: '',
  username: '',
  is_manage: false,
  head_img: "",
  id:""
}

const createMutations = ()=>{
  let res = {};
  for(let i in state_set){
    res[i] = (state, newVal)=>{
      state[i] = newVal
    }
  }
  return res;
}

const createActions = ()=>{
  let res = {};
  for(let i in state_set){
    res['set_'+i] = (ctx, value)=>{
      ctx.commit(i, value)
    }
  }
  return res;
}

export default createStore({
  state:state_set,
  mutations: {
    ...createMutations()
  },
  actions: {
    reset(ctx){
      ctx.commit('username',"")
      ctx.commit('id',"")
      ctx.commit('token',"")
      ctx.commit('head_img',"")
      ctx.commit('is_manage',false)
    },
    ...createActions()
  },
  plugins: [createPersistedState()]
})
