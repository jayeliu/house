module.exports = {
  "presets": [
    "@vue/cli-plugin-babel/preset"
  ],
  "plugins": [
    [
      "component",
      {
        "libraryName": "element-plus",
        "styleLibraryName": "theme-chalk"
      }
    ]
  ],

  "presets": [
    '@vue/cli-plugin-babel/preset'
  ],
  "plugins": [
    ...require('@xdh/my/core/babel.plugins')
  ]
}