const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const path = require('path')
const name = '北上二手房' // 标题

module.exports = {
  // // 部署生产环境和开发环境下的URL。
  // // 默认情况下，Vue CLI 会假设你的应用是被部署在一个域名的根路径上
  // publicPath: './admin/',
  outputDir:'dist',//打包的时候生成的一个文件名

  // webpack-dev-server 相关配置
  devServer: {
    host: 'localhost',
    port: 8088,
    https: false,
    hotOnly: false,
    open: true,
    proxy: 'http://localhost:8083'
  },
  configureWebpack: {
    name: name,
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      }
    }
  },
  configureWebpack: config => {
    if (process.env.NODE_ENV === "production") {
      // 为生产环境修改配置...
      config.mode = "production";
      // 这里修改下 
      config.optimization.minimizer = [
        new UglifyJsPlugin({
          uglifyOptions: {
            warnings: false,
            compress: {
              drop_console: true, //console
              drop_debugger: true,
              pure_funcs: ['console.log'] //移除console
            }
          }
        })
      ]
      //打包文件大小配置
      config["performance"] = {
        "maxEntrypointSize": 10000000,
        "maxAssetSize": 30000000
      }
    } else {
      // 为开发环境修改配置...
      config.mode = "development";
    }
  },

  transpileDependencies: ['@xdh/my'],
  chainWebpack(chain) {
    chain.resolve.alias.set('$ui', '@xdh/my/ui/lib')
  }
}