import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const Plots = ({ plotData }) => {
    const chartRef = useRef(null);

    useEffect(() => {
        if (plotData) {
            if (chartRef.current !== null) {
                chartRef.current.destroy();
            }

            const data = {
                labels: ['lower class', 'count_1', 'count_2', 'count_3', 'count_4', 'count_5'],
                datasets: [{
                    data: [
                        plotData.count_0,
                        plotData.count_1,
                        plotData.count_2,
                        plotData.count_3,
                        plotData.count_4,
                        plotData.count_5
                    ],
                    backgroundColor: [
                        'red',
                        'blue',
                        'green',
                        'orange',
                        'purple',
                        'yellow'
                    ]
                }]
            };

            const ctx = document.getElementById('pieChart').getContext('2d');
            chartRef.current = new Chart(ctx, {
                type: 'pie',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }, [plotData]);

    return (
        <div>
            <h2>Pie Chart</h2>
            <div>
                <canvas id="pieChart" width="400" height="400"></canvas>
            </div>
        </div>
    );
};

export default Plots;
