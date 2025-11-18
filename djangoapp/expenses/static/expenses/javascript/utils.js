export function currency_status(ticks_status){
    
    // Tranfform unity to Real Brazilian
    const currency = new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    })

    if (ticks_status ==  true) {
        const ticks = {
                        callback:(value) => currency.format(value)
                    }
        return ticks
    }
    else {
        const ticks = {}
        return ticks
    }
}