
document.addEventListener('DOMContentLoaded', function() {
    async function ActividadesPorDia() {
        
        try {
            const response = await fetch('/get-stats-data');
            
            const data = await response.json(); 
          
            const chartData = data.map(item => {
                
                const dateParts = item.date.split('-');
                const year = parseInt(dateParts[0]);
                const month = parseInt(dateParts[1]) - 1; 
                const day = parseInt(dateParts[2]);
                const timestamp = Date.UTC(year, month, day);
                return [timestamp, item.count];
            });

 
            Highcharts.chart('first-container', {
                chart: {
                    type: 'line',
                    zoomType: 'x' 
                },
                title: {
                    text: 'Cantidad de actividades por Día',
                    style: {
                        color: '#333'
                    }
                },
                xAxis: {
                    type: 'datetime', 
                    dateTimeLabelFormats: {
                        day: '%e %b', 
                        week: '%e %b',
                        month: '%b \'%y',
                        year: '%Y'
                    },
                    title: {
                        text: 'Día'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Cantidad de actividades'
                    },
                    min: 0, 
                    allowDecimals: false 
                },
                legend: {
                    enabled: false 
                },
                series: [{
                    name: 'Actividades',
                    data: chartData,
                    color: '#4BC0C0', 
                    marker: {
                        enabled: true 
                    }
                }],
               
            });

        } catch (error) {
            console.error('Error al cargar los datos del gráfico:', error);
        }
    }

   async function ActividadesPorTipo() {
        try {
            const response = await fetch('/get-type-activity'); 
        
            const data = await response.json();

            
            const chartData = data.map(item => ({
                name: item.type, 
                y: item.count    
            }));

            Highcharts.chart('second-container', { 
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie' 
                },
                title: {
                    text: 'Total de Actividades por Tipo',
                    align: 'center',
                    style: {
                        color: '#333'
                    }
                },
                
                accessibility: {
                    point: {
                        valueSuffix: '%'
                    }
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %', 
                            distance: -50, 
                            style: {
                                color: 'white',
                                textOutline: '2px solid black' 
                            }
                        },
                        showInLegend: true 
                    }
                },
                series: [{
                    name: 'Porcentaje',
                    colorByPoint: true, 
                    data: chartData
                }],
                
            });

        } catch (error) {
            console.error('Error al cargar los datos del gráfico por tipo:', error);
        }
    }

async function actividadesPorHoraYMes() {
        try {
            const response = await fetch('/get-timed-activities');
            
            const data = await response.json();

            const categories = data.map(item => item.month_label);
            const morningData = data.map(item => item.mañana);
            const middayData = data.map(item => item.mediodia);
            const afternoonData = data.map(item => item.tarde);

            Highcharts.chart('third-container', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Actividades por mes y horario',
                    align: 'center',
                    style: {
                        color: '#333'
                    }
                },
                xAxis: {
                    categories: categories,
                    title: {
                        text: 'Mes'
                    }
                },
                yAxis: {
                    min: 0,
 
                    title: {
                        text: 'Cantidad de actividades'
                    }
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0,
                        groupPadding: 0.1,
                       
                        pointWidth: 15, 
                        minPointLength: 3 
                    }
                },
                series: [{
                    name: 'Mañana',
                    data: morningData,
                    color: '#64B5F6'
                }, {
                    name: 'Mediodía',
                    data: middayData,
                    color: '#FFD54F'
                }, {
                    name: 'Tarde',
                    data: afternoonData,
                    color: '#BA68C8'
                }],
                
            });

        } catch (error) {
            console.error('Error al cargar los datos del gráfico por franja horaria:', error);
        }
    }

   
    ActividadesPorDia();
    ActividadesPorTipo();
    actividadesPorHoraYMes();
});

