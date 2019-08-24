const {Chart} = require('../models/chart')
const {TrackBasicInfo} = require('../models/trackBasicInfo')


function createChartInfo(chartInfo){
    return new Promise((resolve, reject) => {
        var trackId = chartInfo.track_id;
        var trackBasicInfoId = null
    
        getTrackBasicInfoId(trackId, chartInfo).then((trackBasicInfoId) => {
            var newChart = Chart({
                track_basic_info_id : trackBasicInfoId,
                date : chartInfo.date,
                chart_position : chartInfo.track_chart_position,
                number_of_streams: chartInfo.track_number_of_streams,
                trend : chartInfo.trend
            })
            newChart.save().then((chartSaved) => {
                console.log("NewChart Cadastrado!")
                resolve()
            }).catch((e) => {
                reject(e)
            })
        })
    }).catch((e) => {
        console.log("Problema na promise: " + chartInfo + "\n")
        console.log(e.message)
        reject(e)
    })
}

function getTrackBasicInfoId(trackId, chartInfo){
    return new Promise((resolve, reject) => {
        TrackBasicInfo.findOne({spotify_track_id : trackId}).then((track) => {
            if (track === null) {
                console.log("Entrou no if")
                var newTrackBasicInfo = TrackBasicInfo({
                    spotify_track_id : trackId,
                    name: chartInfo.track_name,
                    artist: chartInfo.track_artist,
                    track_link: chartInfo.track_link,
                    track_image: chartInfo.track_image_path
                })

                newTrackBasicInfo.save().then((newTrack) => {
                    console.log("Nova track basic info cadastrada!" + newTrack.name)
                    resolve(newTrack._id)
                }).catch((e) => {
                    console.log("Erro no cadastro do TrackBasicInfo")
                    reject(e)
                })
            } else {
                console.log(track)
                console.log("humm")
                resolve(track._id)
            }
        }).catch((e) => {
            console.log("erro getTrackBasicInfo")
            console.log(e)
            reject(e)
        })
    }).catch((e) => {
        console.log(e)
        console.log("Não achou nada")
        reject(e)
    })
}

module.exports = {createChartInfo}