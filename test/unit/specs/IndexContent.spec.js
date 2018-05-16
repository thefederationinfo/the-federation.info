import Vue from 'vue'

import IndexContent from '@/components/IndexContent'

describe('IndexContent', () => {
    it('should render', () => {
        const Constructor = Vue.extend(IndexContent)
        const vm = new Constructor().$mount()
        expect(vm.$el.querySelector('.main-title h2').textContent)
            .to.equal('Welcome to the new social web')
    })
})
