import axios from 'axios';

export function sendMessage(sender, message) {
    return axios.post(`http://10.195.48.145:7892/api/chat`, {sender, message})
}