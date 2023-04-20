import settings from '@/common/settings'
import { createRouter, createWebHistory, type HistoryState, type RouteLocationNormalized } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    }
  ]
})

export function routeTo(path: string, metaData?: HistoryState) {
  router.push({ name: path, state: { meta: metaData } })
}

export async function conditionalRouteTo(
  next: (arg0?: RouteLocationNormalized | string) => any,
  conditionFunc: () => Promise<boolean>,
  correctRoute?: RouteLocationNormalized | string | null,
  incorrectRoute?: RouteLocationNormalized | string | null
) {
  if (settings.DEBUG) {
    next()
    return
  }
  const to = (await conditionFunc()) ? correctRoute : incorrectRoute
  if (to) {
    next(to)
  } else {
    next()
  }
}

export function urlRelativeTo(rootUrl: string, url: string) {
  url = url.slice(url.indexOf(rootUrl) + rootUrl.length)
  return url.startsWith('/') ? url.slice(1) : url
}

export default router
