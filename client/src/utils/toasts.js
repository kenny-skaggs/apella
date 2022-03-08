
const level = {
    error: 1,
    warning: 2,
    info: 3
}

function Toast(message, level) {
    return {
        message: message,
        level: level
    }
}

export default {
    Toast,
    level
}
