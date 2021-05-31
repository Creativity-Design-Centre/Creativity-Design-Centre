<template>
  <div class="search-component-container">
    <div class="search-out-container">
      <a-modal
        id="change-image"
        title="Title"
        :visible="dialogVisable"
        @ok="handleOk"
        @cancel="handleCancel"
      >
        <div class="image-container">
          <VueDragResize
            :isActive="true"
            :w="200"
            :h="200"
            v-on:resizing="resize"
            v-on:dragging="resize"
            v-for="i in showImage"
            v-bind:key="i"
            :style="`background-image: url(${i}); background-repeat: no-repeat; background-size: cover`"
          ></VueDragResize>
        </div>
      </a-modal>
      <a-input-search
        class="search-item"
        placeholder="input search text"
        @search="onSearch"
        enterButton="Search"
        size="large"
      />
    </div>
    <div class="selected-container">
      <a-tag
        closable
        v-for="i in confirmResult"
        v-bind:key="i"
        @close="cancelAdd(i)"
        >{{ i }}</a-tag
      >
    </div>
    <a-button class="generate-btn" type="primary" block @click="generate"
      >生成图片</a-button
    >
    <div class="tag-container">
      <a-popover
        class="tag-item"
        v-for="i in searchResult"
        v-bind:key="i.term"
        v-on:click="confirmAdd(i.end.label)"
      >
        <template slot="content">{{ i.surfaceText }}</template>
        <a-button type="primary">{{ i.end.label }}</a-button>
      </a-popover>
      <a-popover
        class="tag-item"
        v-for="i in searchResult"
        v-bind:key="i.term"
        v-on:click="confirmAdd(i.start.label)"
      >
        <template slot="content">{{ i.surfaceText }}</template>
        <a-button type="success">{{ i.start.label }}</a-button>
      </a-popover>
    </div>
  </div>
</template>

<script>
import VueDragResize from 'vue-drag-resize'

export default {
  name: 'Search',
  data: function () {
    return {
      hasResult: false,
      searchResult: [],
      confirmResult: ['https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1922912628,3118313769&fm=26&gp=0.jpg', 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2374596061,3372688405&fm=26&gp=0.jpg'],
      showImage: ['https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1922912628,3118313769&fm=26&gp=0.jpg', 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=2374596061,3372688405&fm=26&gp=0.jpg'],
      searchStatus: false,
      dialogVisable: true
    }
  },
  components: {
    VueDragResize
  },
  mounted () {
    //this.googleSearch('car')
  },
  methods: {
    onSearch (v) {
      const self = this
      let inputVaule = v.replace(/(^\s*)|(\s*$)/g, '')
      inputVaule = inputVaule.replace(' ', '_')
      self.$axios
        .get('http://127.0.0.1:5000/search', {
          params: {
            keyword: inputVaule
          }
        })
        .then(res => {
          // eslint-disable-next-line no-console
          let rlt = res.data
          self.searchResult = rlt.edges
          // eslint-disable-next-line no-console
          console.log(rlt)
        })
    },
    generate () {
      const self = this
      const len = self.confirmResult.length
      let promiseArr = []
      if (self.searchStatus) {
        self.$message.error(`in processing`)
        return
      }
      if (len <= 1) {
        self.$message.error(`pick enough concept, at least 2`)
        return
      }
      self.searchStatus = true
      for (let i = 0; i < len; i++) {
        let pitem = self.confirmResult[i]
        let pwait = self.googleSearch(pitem)
        promiseArr.push(pwait)
      }
      Promise.all(promiseArr).then(res => {
        // eslint-disable-next-line no-console
        if (res[0] == true && res[1] == true) {
          self.dialogVisable = true;
        }
      })
    },
    resize () { },
    googleSearch (key) {
      const self = this
      let re = new Promise(resolve => {
        self.$axios
          .get('http://127.0.0.1:5000/get_image', {
            params: {
              keyword: key
            }
          })
          .then(res => {
            let len = res.data.data.length
            if (len <= 0) {
              self.$message.error(`${key} has no image`)
            }
            let randomNum = Math.floor(Math.random() * len)
            let imgUrl = res.data.data[randomNum]
            self.showImage.push(imgUrl)
            resolve(true)
            // eslint-disable-next-line no-console
            // console.log(res.data.list[randomNum].cover_imgurl)
          })
      })
      return re
    },
    confirmAdd (a) {
      const self = this
      self.confirmResult.push(a)
    },
    cancelAdd (a) {
      const self = this
      let index = self.confirmResult.indexOf(a)
      self.confirmResult.splice(index, 1)
    },
    handleOk () {
      const self = this;
      self.dialogVisable = false;
      self.searchStatus = false;
    },
    handleCancel () {
      const self = this;
      self.dialogVisable = false;
      self.searchStatus = false;
    }
  }
}
</script>

<style>
.search-component-container {
  width: 80%;
  margin: 0 auto;
  padding-top: 40px;
}
.search-out-container {
  width: 100%;
}
.search-container {
  position: absolute;
}
.ant-modal-body {
  position: relative;
  height: 600px;
}
.generate-btn {
  height: 40px !important;
  margin-top: 10px;
  margin-bottom: 10px;
}
.tag-container {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-top: 20px;
  overflow: hidden;
}
.drag-image {
  width: 200px;
  height: 200px;
}
.tag-item {
  margin: 5px 0;
}
.image-container {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
