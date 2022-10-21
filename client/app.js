const App = {
    el: '#app',
    data () {
        return {
            debug: '', 
            searchBox: null, 
            selectedPlatform: 'youtube',
            search: { platforms: ['youtube','podcast','radio'] },
            results: { search: [] },
            isActive: false
        } 
    },
    mounted() {
        this.searchBox = document.getElementById('search')
    },
    methods: {
        doSearch(ev) {
            axios.get('http://localhost:8000/server/search/', { params: { query: this.searchBox.value, platform: this.selectedPlatform } }).then(res=>{
                console.log(res.data)
                this.results.search = res.data
            })
        },
        play(arg) {
            if (arg.platform == 'podcast') {
                axios.get('http://localhost:8000/server/episodes/', { params: { url: arg.url } }).then(res=>{
                    console.log(res.data)
                    this.results.search = res.data
                })
            } else {
                axios.get('http://localhost:8000/server/play/', { params: { url: arg.url, platform: arg.platform } }).then(res=>{
                    this.results.search = []
                    this.isActive = true
                })
            }
        },
        selectPlatform(platform) {
            this.selectedPlatform = platform
        },
        pause(arg) {
            axios.get('http://localhost:8000/server/pause/')
            this.isActive = !this.isActive
        }
    }
}

const app = Vue.createApp(App)
app.mount('#app')
