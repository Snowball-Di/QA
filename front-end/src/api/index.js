import axios from 'axios';
import  { API_HOST } from "../config.json"

export function sendMessage(sender, message) {
    return axios.post(`${API_HOST}/chat`, {sender, message})
}

export function sendAudio(time, size, pcmBlob) {
    var audio = new FormData()
    audio.append('file', pcmBlob,"1.pcm")
    audio.append('time', time)
    audio.append('size', size)
    return axios.post(`${API_HOST}/sendaudio`, audio)
}

export function sendphoto(photoblob) {
    var photo = new FormData()
    photo.append('file', photoblob, "1.jpg")
    photo.append('type', 'photo')
    return axios.post(`${API_HOST}/sendphoto`, photo)
}

