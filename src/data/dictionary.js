/** @template K, V */
class Dictionary {

    #data = {}

    /**
     * @param {K} key
     * @return {V}
     */
    get(key){
        return this.#data[key]
    }

    /**
     * @param {K} key
     * @param {V} value
     */
    set(key, value){
        this.#data[key] = value
    }

    /** @return {Array<V>} */
    get values(){
        return Object.values(this.#data)
    }

    get keys(){
        return Object.keys(this.#data)
    }

    /**
     * @param {V} value
     * @return {K|null}
     */
    getKey(value){
        const keys = this.keys
        return keys.find( (k) => this.#data[k] === value )
    }

    /**
     * @template item
     * @callback GetK
     * @param {item} Obj
     * @returns {K}
     */

    /**
     * @template item
     * @callback GetV
     * @param {item} Obj
     * @returns {V}
     */

    /**
     * @template item
     * @param {Array<item>} array
     * @param {GetK<item>} getKey
     * @param {GetV<item>} getValue
     */
    import(array, getKey, getValue){

        array.forEach( (item) => {
            const key = getKey(item)
            const value = getValue(item)

            this.set(key, value)
        })
    }

    map( callback ){
        const keys = this.keys
        return keys.map( (key) => {
            const value = this.#data[key]
            return callback( value, key )
        })
    }

    /**
     * @callback Filter
     * @param {V} Obj
     * @returns {Boolean}
     */

    /**
     * @param {Filter} callback
     * @return {Array<V>}
     */
    filter(callback){
        const values = this.values
        return values.filter( (value) => callback(value) )
    }
}

export default Dictionary