<script setup lang="ts">
import { reactive, ref } from 'vue'
import axios from 'axios'

const values = reactive({
  member: {
    id: ''
  },
  request: {
    count: 1,
    interval: 2.0,
    submit_interval: 0.5,
    answer_time: 8.0,
    consistent_time: false,
    correct_rate: 0.9
  },
  normal_distribution: {
    enabled: true,
    answer_time_scale: 0.75,
    correct_rate_scale: 0.03
  },
  cookies: {
    session: ''
  }
})

// const output = ref(
//   '1: {"examCount":[1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,2,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],"isExamRepeat":false,"subId":"1649016858665152514","userCorrectCount":44,"userErrorCount":6} 总耗时: 0:00:01.315653 执行完毕'
// )
// const finished = ref(true)
const output = ref('')
const finished = ref(false)

async function onSubmit() {
  finished.value = false
  output.value = '执行中, 请等待...'
  const response = await axios.post('/submitexam', values)
  output.value = `${response.data}\n执行完毕`
  finished.value = true
}
</script>

<template>
  <main class="u-grid u-w-full u-h-full u-bg-truegray-800 u-text-truegray-300 u-overflow-hidden">
    <div
      v-if="!output"
      class="main u-flex u-flex-col u-justify-self-center u-self-center u-min-w-full sm:u-min-w-360px u-max-h-[calc(100%-24px)] sm:u-rounded-md u-overflow-hidden"
    >
      <div class="main-inner u-p-4">
        <form
          class="u-flex u-flex-col u-gap-2"
          id="form1"
          action="/submitexam"
          method="post"
          onsubmit="return false"
          @submit="onSubmit"
        >
          <div class="group">
            <div class="u-text-center u-border-b-1">会员</div>
            <label class="input-container">
              <div class="input-title" title="会员卡ID">会员卡</div>
              <input
                v-model="values.member.id"
                type="text"
                name=""
                id=""
                autocomplete="new-password"
              />
            </label>
          </div>

          <div class="group">
            <div class="u-text-center u-border-b-1">Request</div>
            <label class="input-container">
              <div class="input-title" title="次数">次数</div>
              <input v-model="values.request.count" type="number" name="" id="" min="1" max="999" />
            </label>
            <label class="input-container">
              <div class="input-title" title="每次答题的时间间隔">时间间隔</div>
              <input
                v-model="values.request.interval"
                type="number"
                name=""
                id=""
                min="0.0"
                max="999.0"
                step="0.01"
              />
            </label>
            <label class="input-container">
              <div class="input-title" title="请求和提交的时间间隔">提交延迟</div>
              <input
                v-model="values.request.submit_interval"
                type="number"
                name=""
                id=""
                min="0.0"
                max="999.0"
                step="0.01"
              />
            </label>
            <label class="input-container">
              <div class="input-title" title="答题时间">答题时间</div>
              <input
                v-model="values.request.answer_time"
                type="number"
                name=""
                id=""
                min="0.0"
                max="999.0"
                step="0.1"
              />
            </label>
            <label class="input-container">
              <div class="input-title" title="是否让提交延迟时间与答题时间保持一致">时间拟真</div>
              <input v-model="values.request.consistent_time" type="checkbox" name="" id="" />
            </label>
            <label class="input-container">
              <div class="input-title" title="正确率">正确率</div>
              <input
                v-model="values.request.correct_rate"
                type="number"
                name=""
                id=""
                min="0.0"
                max="1.0"
                step="0.02"
              />
            </label>
          </div>

          <div class="group">
            <div class="u-text-center u-border-b-1">正态分布随机数</div>
            <label class="input-container">
              <div class="input-title" title="Session id">启用</div>
              <input v-model="values.normal_distribution.enabled" type="checkbox" name="" id="" />
            </label>
            <label class="input-container">
              <div class="input-title" title="答题时间正太分布比例">答题时间正太比例</div>
              <input
                v-model="values.normal_distribution.answer_time_scale"
                type="number"
                name=""
                id=""
                min="0.0"
                max="999.0"
                step="0.01"
              />
            </label>
            <label class="input-container">
              <div class="input-title" title="正确率正太分布比例">正确率正太比例</div>
              <input
                v-model="values.normal_distribution.correct_rate_scale"
                type="number"
                name=""
                id=""
                min="0.0"
                max="999.0"
                step="0.01"
              />
            </label>
          </div>

          <div class="group">
            <div class="u-text-center u-border-b-1">Cookies</div>
            <label class="input-container">
              <div class="input-title" title="Session id">session</div>
              <input
                v-model="values.cookies.session"
                type="text"
                name=""
                id=""
                autocomplete="new-password"
              />
            </label>
          </div>

          <div class="group">
            <input
              class="u-bg-green-600 u-py-2 u-rounded-lg u-cursor-pointer"
              type="submit"
              value=""
            />
          </div>
        </form>
      </div>
    </div>
    <div v-else class="u-overflow-auto">
      <pre>{{ output }}</pre>
      <div v-if="finished" class="u-flex u-justify-center">
        <button class="u-px-4 u-py-2 u-bg-blue-600 u-rounded-lg" @click="output = ''">完成</button>
      </div>
    </div>
  </main>
</template>

<style lang="scss" scoped>
.main {
  box-shadow: 0 0 16px #0f06;
}

.main-inner {
  height: 100%;
  overflow: auto;
}

.main-inner::-webkit-scrollbar {
  background-color: transparent;
}

.main-inner::-webkit-scrollbar-thumb {
  background-color: #8883;
}

.group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 8px 0;
}

.input-container {
  padding: 2px 8px;
  z-index: 0;
  position: relative;
  display: flex;
}

.input-container {
  input[type='text'],
  input[type='number'] {
    width: 100%;
    overflow: hidden;
    background: transparent;
  }
}

.input-container::before {
  z-index: -1;
  content: '';
  display: block;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 4px;
  box-shadow: 0 0 10px #00f, 0 0 20px #00f;
  opacity: 0;
  transition: all 0.15s ease-in-out;
}

.input-container {
  &:has(input:focus)::before,
  &:is(:hover)::before {
    opacity: 1;
  }
}

.input-title {
  margin-right: 8px;
  color: #b7b7b7;
  min-width: 80px;
  white-space: nowrap;
  flex-shrink: 0;
  transition: all 0.15s ease-in-out;
}

.input-container:has(input:focus) .input-title {
  color: #fff;
}
</style>
