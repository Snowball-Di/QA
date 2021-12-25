import axios from 'axios';
import  { API_HOST } from "../config.json"

export function sendMessage(sender, message) {
    return axios.post(`${API_HOST}/chat`, {sender, message})
}