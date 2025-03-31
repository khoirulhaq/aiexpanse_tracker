// Function untuk mendapatkan parameter filter dari URL
function getFilterParams() {
    const params = new URLSearchParams(window.location.search);
    const start_date = params.get("start_date") || "";
    const end_date = params.get("end_date") || "";
    const description = params.get("description") || "";
    return { start_date, end_date, description };
}

// Initialize Line Chart
let lineChart;
async function initializeLineChart() {
    const chartData = await fetchLineChartData();

    lineChart = echarts.init(document.getElementById('AN-LineChart'));
    const lineOption = {
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: chartData.labels // Bulan-bulan sebagai sumbu x
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: 'Total Expenses',
                type: 'line',
                data: chartData.values, // Nilai nominal sebagai sumbu y
                smooth: true,
                lineStyle: {
                    width: 3
                }
            }
        ]
    };
    lineChart.setOption(lineOption);
}

// Initialize Doughnut Chart
let doughnutChart;
async function initializeDoughnutChart() {
    const chartData = await fetchDoughnutChartData();

    doughnutChart = echarts.init(document.getElementById('AN-DoghnutChart'));
    const doughnutOption = {
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                // Format nilai sebagai currency
                const formattedValue = new Intl.NumberFormat('id-ID', {
                    style: 'currency',
                    currency: 'IDR'
                }).format(params.value);

                // Tampilkan nama dan nilai dalam format currency
                return `${params.name} <br/> ${formattedValue}`;
            }
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                name: 'Dompet',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 20,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: chartData.labels.map((label, index) => ({
                    name: label,
                    value: chartData.values[index]
                }))
            }
        ]
    };
    doughnutChart.setOption(doughnutOption);
}
// Fetch data untuk Line Chart
async function fetchLineChartData() {
    const { start_date, end_date, description } = getFilterParams();
    const response = await fetch(`/api/analytics-line-chart-data?start_date=${start_date}&end_date=${end_date}&description=${description}`);
    const data = await response.json();
    return data;
}

// Fetch data untuk Doughnut Chart
async function fetchDoughnutChartData() {
    const { start_date, end_date, description } = getFilterParams();
    const response = await fetch(`/api/analytics-doughnut-chart-data?start_date=${start_date}&end_date=${end_date}&description=${description}`);
    const data = await response.json();
    return data;
}

// Menambahkan event listener untuk resize
window.addEventListener('resize', function () {
    if (lineChart) lineChart.resize();
    if (doughnutChart) doughnutChart.resize();
    // Jika ada grafik lain di masa depan, tambahkan di sini:
    // if (Prioritas) Prioritas.resize();
    // if (barChart) barChart.resize();
});

// Initialize semua grafik saat halaman dimuat
document.addEventListener('DOMContentLoaded', async () => {
    await initializeLineChart();
    await initializeDoughnutChart();
});