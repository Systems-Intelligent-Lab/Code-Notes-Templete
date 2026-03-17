import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/Code-Notes-Templete/',
  title: 'Code Notes',
  description: 'Python 代码笔记与示例',
  lang: 'zh-CN',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: 'Python 基础', link: '/python-basics/default_args' }
    ],
    sidebar: {
      '/python-basics/': [
        {
          text: 'Python 基础',
          items: [
            { text: '默认参数示例', link: '/python-basics/default_args' }
          ]
        }
      ],
      '/': [
        {
          text: '指南',
          items: [{ text: '简介', link: '/' }]
        }
      ]
    }
  }
})

