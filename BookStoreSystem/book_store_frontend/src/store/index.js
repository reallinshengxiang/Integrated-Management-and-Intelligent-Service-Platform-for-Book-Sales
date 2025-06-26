import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

const state_set = {
  token: '',
  username: '',
  id: "",
  
  modifyid: -1,
  detailid: 92555
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

const store = createStore({
  state: state_set,
  mutations: {
    ...createMutations()
  },
  actions: {
    reset(ctx){
      ctx.commit('username', "")
      ctx.commit('id', "")
      ctx.commit('token', "")
      // 重置新变量
      ctx.commit('modifyid', -1)
    },
    ...createActions()
  },
  plugins: [createPersistedState()]
})

export default store;
