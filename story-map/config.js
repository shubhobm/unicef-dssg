var config = {
    style: 'mapbox://styles/christinaklast/ckliegjeo1d4z17obxhgzzs90',
    accessToken: 'pk.eyJ1IjoiY2hyaXN0aW5ha2xhc3QiLCJhIjoiY2tsaHAzM3gyMDg5bTJ2cWloOGNwOGw1ayJ9.J4_TjIpU5bmH9qO7WRLteQ',
    showMarkers: false,
    theme: 'dark',
    use3dTerrain: true,
    title: 'Air Quality Monitoring Platform',
    subtitle: 'Measuring the effect of COVID-19 lockdowns on air quality and the exposure of child populations using machine learning',
    byline: '',
    footer: 'Source: Data generated from Last et. al (2021) <a href="https://github.com/shubhobm/air-pollution-draft"</a>. Data available <a href="https://github.com/shubhobm/unicef-dssg</a>',
    chapters: [
        {
            id: 'global-intro',
            alignment: 'left',
            title: 'Objective',
            description: 'UNICEF and Solve for Good have partnered together to analyze various aspects of changes in air pollution — especially related to COVID-19 and with the long-term goal to build a platform for air pollution monitoring with a strong emphasis on UNICEF’s operations. In this storymap, we demonstrate the results from a machine learning model predicting PM2.5 concentrations. We then measure children’s exposure to air pollutant PM2.5, which exceeds the WHO Standard in the present COVID Scenario. We developed this platform to understand concerntrations of PM2.5 around the globe with the target of attaining a fine-grained estimation from the combination of Ground value measurement from openly available ground sensor measurements and Remote Sensing, and enable Citizen Scientists to delve deeper and get involved in Air Quality Measurement globally.',
            location: {
                center: [
                    15.01780, 22.78995
                ],
                zoom: 1.47,
                pitch: 0.00,
                bearing: 0.00
            },
            onChapterEnter: [
              {
                layer: '10_vietnam_week_6',
                opacity: 0
              }, {
                  layer: '10_vietnam_week_16',
                  opacity: 0
              }, {
                  layer: '10_peru_week_6',
                  opacity: 0
              }, {
                  layer: '10_peru_week_16',
                  opacity: 0
              }, {
                  layer: '10_sierra_leone_week_16',
                  opacity: 0
              }, {
                  layer: '10_sierra_leone_week_6',
                  opacity: 0
              },
            ],
            onChapterExit: [

            ]
        }, {
            id: 'global-method',
            alignment: 'left',
            image: '',
            description: 'According to the WHO guidelines, PM2.5 is identified as one of the most dangerous pollutants for human health. We use the WHO measure of high exposure to PM2.5 (10 μg/m3 annual mean) and (25 μg/m3 24-hour mean) to identify locations of high exposure to PM2.5 in the countries UNICEF have regional offices in.',
            location: {
                center: [
                    15.01780, 22.78995
                ],
                zoom: 1.47,
                pitch: 0.00,
                bearing: 0.00
            },
            onChapterEnter: [],
            onChapterExit: [
                // {
                //     layer: 'gnpglaciers-2015',
                //     opacity: 0
                // }
            ]
        }, {
            id: 'vietnam-week-6',
            alignment: 'left',
            title: 'Vietnam, week beginning February 3, 2020',
            image: '',
            description: 'Here is data displaying the regions of high exposure to PM2.5 concentrations (in peach are areas above weekly average 10 μg/m3 and in orange areas experiencing a weekly average PM2.5 concentration above 25 μg/m3.',
            location: {
                center: [
                    103.55332, 16.72187
                ],
                zoom: 5.28,
                pitch: 39.50,
                bearing: 36.00
            },
            onChapterEnter: [
              {
                layer: '10_vietnam_week_6',
                opacity: 0.55
              }, {
                layer: '25_vietnam_week_6',
                opacity: 0.55
              }
            ],
            onChapterExit: [
                // {
                //     layer: '10_vietnam_week_6',
                //     opacity: 0
                // }, {
                //   layer: '25_vietnam_week_6',
                //   opacity: 0
                // }
            ]
        }, {
            id: 'ho-chi-minh-2020-feb',
            alignment: 'left',
            title: 'Ho Chi Minh, February 3rd 2020',
            image: '',
            description: 'In early february a weekly average of over 16,000,000 children were exposed to high levels of PM2.5. This covers most of the metrpolitan area of Ho Chi Minh city, with hotspots of acutely high levels (> 25 μg/m3) of PM2.5 in several central city locations.',
            location: {
                center: [
                    106.26967, 10.03260
                ],
                zoom: 8.36,
                pitch: 57.50,
                bearing: -90.36
            },
            onChapterEnter: [
                {
                  layer: '10_vietnam_week_6',
                  opacity: 0.55
                }, {
                  layer: '25_vietnam_week_6',
                  opacity: 0.55
                },{
                  layer: '10_vietnam_week_16',
                  opacity: 0
                }, {
                  layer: '25_vietnam_week_16',
                  opacity: 0
                }
            ],
            onChapterExit: [
              {
                layer: '10_vietnam_week_6',
                opacity: 0
              }, {
                layer: '25_vietnam_week_6',
                opacity: 0
              },{
                layer: '10_vietnam_week_16',
                opacity: 0.55
              }, {
                layer: '25_vietnam_week_16',
                opacity: 0.55
              }
            ]
        }, {
            id: 'ho-chi-minh-2020-april',
            alignment: 'left',
            title: 'Ho Chi Minh, April 16th 2020',
            image: '',
            description: 'On March 30th, Vietnam announced a lockdown due to the spread of COVID-19. On the week beginning the 13th Aprikl, there are dramatic reductions in the level of exposure to high levels of PM2.5, as 4,000,000 children expereieced a reduction in exposure to (> 10 μg/m3) of PM2.5 in several central city locations.',
            location: {
                center: [
                    106.26967, 10.03260
                ],
                zoom: 8.36,
                pitch: 57.50,
                bearing: -90.36
            },
            onChapterEnter: [
              {
                layer: '10_vietnam_week_16',
                opacity: 0.55
              }, {
                layer: '25_vietnam_week_16',
                opacity: 0.55
              }, {
                layer: '10_vietnam_week_6',
                opacity: 0
              }, {
                layer: '25_vietnam_week_6',
                opacity: 0
              }
            ],
            onChapterExit: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0
                }
            ]
        }, {
            id: 'agassiz1998',
            alignment: 'left',
            title: 'Agassiz Glacier, 1998',
            image: '',
            description: 'Agassiz Glacier is in Glacier National Park in the U.S. state of Montana. It is named after Louis Agassiz, a Swiss-American glaciologist. The glacier is situated in a cirque to the southeast of Kintla Peak west of the Continental Divide. Agassiz Glacier is one of several glaciers that have been selected for monitoring by the U.S. Geological Survey\'s Glacier Monitoring Research program, which is researching changes to the mass balance of glaciers in and surrounding Glacier National Park.',
            location: {
                center: [
                    -114.15881, 48.93439
                ],
                zoom: 13.51,
                pitch: 41.00,
                bearing: 78.33
            },
            onChapterEnter: [],
            onChapterExit: []
        }, {
            id: 'agassiz2015',
            alignment: 'left',
            title: 'Agassiz Glacier, 2015',
            image: '',
            description: 'Between 1998 and 2015, Agassiz Glacier lost 108 acres of surface area (about 37%).',
            location: {
                center: [
                    -114.15881, 48.93439
                ],
                zoom: 13.51,
                pitch: 41.00,
                bearing: 78.33
            },
            onChapterEnter: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0.25
                }
            ],
            onChapterExit: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0
                }
            ]
        }, {
            id: 'rainbow1998',
            alignment: 'left',
            title: 'Rainbow Glacier, 1998',
            image: '',
            description: 'Rainbow Glacier is in Glacier National Park in the U.S. state of Montana. The glacier is situated immediately to the east of Rainbow Peak at an elevation between 8,500 feet (2,600 m) and 8,000 feet (2,400 m) above sea level. The glacier has visible crevasses in satellite imagery. Rainbow Glacier has shown modest retreat compared to other glaciers in Glacier National Park.',
            location: {
                center: [
                    -114.08659, 48.88039
                ],
                zoom: 13.09,
                pitch: 50.00,
                bearing: -53.60
            },
            onChapterEnter: [],
            onChapterExit: []
        }, {
            id: 'rainbow2015',
            alignment: 'left',
            title: 'Rainbow Glacier, 2015',
            image: '',
            description: 'Between 1998 and 2015, Rainbow Glacier lost 17 acres of surface area (about 6%).',
            location: {
                center: [
                    -114.08659, 48.88039
                ],
                zoom: 13.09,
                pitch: 50.00,
                bearing: -53.60
            },
            onChapterEnter: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0.25
                }
            ],
            onChapterExit: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0
                }
            ]
        }, {
            id: 'kintla1998',
            alignment: 'left',
            title: 'Kintla Glacier, 1998',
            image: '',
            description: 'Kintla Glacier is in Glacier National Park in the U.S. state of Montana. The glacier is situated on a plateau 2 miles (3.2 km) southwest of Kintla Peak at an elevation between 8,700 feet (2,700 m) and 7,700 feet (2,300 m) above sea level. The glacier has numerous crevasses and is actually two glaciers.',
            location: {
                center: [
                    -114.18755, 48.92880
                ],
                zoom: 13.09,
                pitch: 48.50,
                bearing: 164.00
            },
            onChapterEnter: [],
            onChapterExit: []
        }, {
            id: 'kintla2015',
            alignment: 'left',
            title: 'Kintla Glacier, 2015',
            image: '',
            description: 'Between 1998 and 2015, Harrison Glacier lost 24 acres of surface area (about 10%).',
            location: {
                center: [
                    -114.18755, 48.92880
                ],
                zoom: 13.09,
                pitch: 48.50,
                bearing: 164.00
            },
            onChapterEnter: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0.25
                }
            ],
            onChapterExit: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0
                }
            ]
        }, {
            id: 'sperry1998',
            alignment: 'left',
            title: 'Sperry Glacier, 1998',
            image: '',
            description: 'Sperry Glacier is a glacier on the north slopes of Gunsight Mountain west of the Continental Divide in Glacier National Park in the U.S. state of Montana. Although many geologic features of Glacier National Park were formed during the much longer period of glaciation ending over 10,000 years ago, Sperry Glacier — like all the glaciers in the park today — is a product of the recent Little Ice Age, the period of cooler average temperatures starting in about the 13th century and concluding in the mid-19th century.',
            location: {
                center: [
                    -113.75672, 48.62433
                ],
                zoom: 13.68,
                pitch: 34.50,
                bearing: 106.40
            },
            onChapterEnter: [],
            onChapterExit: []
        }, {
            id: 'sperry2015',
            alignment: 'left',
            title: 'Sperry Glacier, 2015',
            image: '',
            description: 'Between 1998 and 2015, Harrison Glacier lost 37 acres of surface area (about 16%).',
            location: {
                center: [
                    -113.75672, 48.62433
                ],
                zoom: 13.68,
                pitch: 34.50,
                bearing: 106.40
            },
            onChapterEnter: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0.25
                }
            ],
            onChapterExit: [
                {
                    layer: 'gnpglaciers-2015',
                    opacity: 0
                }
            ]
        }
    ]
};
