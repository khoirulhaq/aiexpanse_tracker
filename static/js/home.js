// Fungsi untuk mengambil data dari endpoint API
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}


// Inisialisasi grafik setelah data diterima
async function initializeCharts() {
  const apiData = await fetchData('/api/sales-data'); // Endpoint API dari backend

  if (apiData) {
      // Data diambil dari API
      const categories = apiData.categories; // Misalnya: ['Jan', 'Feb', 'Mar', 'Apr', 'May']
      const salesData = apiData.sales;       // Misalnya: [120, 190, 300, 500, 200]

      // Line Chart (Sales Overview)
      var lineChart = echarts.init(document.getElementById('lineChart'));
      var lineOption = {
          title: {
              text: 'Monthly Expenses'
          },
          tooltip: {
              trigger: 'axis'
          },
          legend: {
              data: ['Expenses']
          },
          xAxis: {
              type: 'category',
              data: categories // Data dari API
          },
          yAxis: {
              type: 'value'
          },
          series: [{
              name: 'Expenses',
              type: 'line',
              data: salesData, // Data dari API
              smooth: true,
              color: '#007BFF'
          }]
      };
      lineChart.setOption(lineOption);

      // Menambahkan event listener resize
      window.addEventListener('resize', function () {
          lineChart.resize(); // Menyesuaikan ukuran grafik saat ukuran jendela berubah
      });
  }
}

// Panggil fungsi untuk memulai grafik
initializeCharts();


// Fungsi untuk memformat angka sebagai mata uang Indonesia
function formatCurrency(value) {
  return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR'
  }).format(value);
}

// Inisialisasi grafik Doughnut setelah data diterima
async function initializeDoughnutChart() {
  const apiData = await fetchData('/api/revenue-data'); // Endpoint API untuk data Revenue Breakdown

  if (apiData) {
      // Data diambil dari API
      const doughnutData = apiData.revenue; // Misalnya: [{value: 300, name: 'Product A'}, ...]

      // Doughnut Chart 1 (Revenue Breakdown)
      var doughnutChart1 = echarts.init(document.getElementById('doughnutChart1'));
      var doughnutOption1 = {
          tooltip: {
              trigger: 'item', // Tooltip muncul saat menghover item
              formatter: function (params) {
                  // Format tooltip dengan nama dan nilai nominal dalam mata uang Indonesia
                  return `${params.name}: ${formatCurrency(params.value)}`;
              }
          },
          legend: {
              top: '5%', // Legend ditempatkan di bagian atas
              left: 'center' // Legend berada di tengah horizontal
          },
          series: [
              {
                  name: 'Revenue',
                  type: 'pie',
                  radius: ['40%', '70%'], // Ukuran pie chart
                  avoidLabelOverlap: false,
                  itemStyle: {
                      borderRadius: 10, // Border melengkung
                      borderColor: '#fff', // Warna border putih
                      borderWidth: 2 // Ketebalan border
                  },
                  label: {
                      show: false, // Label tidak ditampilkan secara default
                      position: 'center'
                  },
                  emphasis: {
                      label: {
                          show: true, // Label muncul saat hover
                          fontSize: 40, // Ukuran font besar
                          fontWeight: 'bold', // Font tebal
                          formatter: function (params) {
                              // Format label dengan nama item
                              return params.name;
                          }
                      }
                  },
                  labelLine: {
                      show: false // Tidak menampilkan garis label
                  },
                  data: doughnutData, // Data dari API
                  color: ['#007BFF', '#28A745', '#FFC107', '#DC3545', '#6C757D'] // Warna tetap atau bisa juga diambil dari API
              }
          ]
      };
      doughnutChart1.setOption(doughnutOption1);
  }
}

// Panggil fungsi untuk memulai grafik
initializeDoughnutChart();


function setTextColor(elementId, value) {
  const element = document.getElementById(elementId);
  
  // Memeriksa apakah nilai berubah positif atau negatif
  if (value.includes('-')) {
    // Jika negatif, beri warna merah
    element.style.color = 'green';
  } else {
    // Jika positif, beri warna hijau
    element.style.color = 'red';
  }
}

// Fetch expenses data from API
fetch('/api/expenses')
  .then(response => response.json())
  .then(data => {
    // Update each card with data
    const monthExpElement = document.getElementById('monthExp');
    const weekExpElement = document.getElementById('weekExp');
    const todayExpElement = document.getElementById('todayExp');

    const avgExpElement = document.getElementById('avgThisMonth');
    const changeInMonthElement = document.getElementById('changeInMonth');
    const changeInWeekElement = document.getElementById('changeInWeek');

    const Exp12MonthElement = document.getElementById('Exp12Month');
    const avgTTMElement = document.getElementById('avgTTM');
    const medianTTMElement = document.getElementById('medianTTM');

    // Mengatur warna teks berdasarkan nilai positif atau negatif
    setTextColor("changeInMonth", data.change_in_month);
    setTextColor("changeInWeek", data.change_in_week);
    
    // Menambahkan class typing-effect untuk memulai animasi pengetikan
    monthExpElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">Rp ${data.month.toLocaleString('id-ID')}</span>
      </div>
    `;
    weekExpElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">Rp ${data.this_week.toLocaleString('id-ID')}</span>
      </div>
    `;
    todayExpElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">Rp ${data.today.toLocaleString('id-ID')}</span>
      </div>
    `;
    avgExpElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">Rp ${data.avg_daily_month.toLocaleString('id-ID')}</span>
      </div>
    `;
    changeInMonthElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">${data.change_in_month}</span>
      </div>
    `;
    changeInWeekElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">${data.change_in_week}</span>
    `;
    Exp12MonthElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">Rp ${data.total_12_months.toLocaleString('id-ID')}</span>
    `;
    avgTTMElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">Rp ${data.average_12_months.toLocaleString('id-ID')}</span>
    `;
    medianTTMElement.innerHTML = `
      <div class="expense-container">
        <span class="typing-effect">Rp ${data.median_12_months.toLocaleString('id-ID')}</span>
    `;

  })
  .catch(error => console.error('Error fetching expenses data:', error));


// Bar Chart (Monthly Category Spending)
var barChart = echarts.init(document.getElementById('barChart'));

async function fetchMonthlyCategoryData() {
    const response = await fetch('/api/monthly-category-data');
    const data = await response.json();
    return data;
}

async function initializeBarChart() {
    const chartData = await fetchMonthlyCategoryData();

    // Konfigurasi ECharts
    const barOption = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: chartData.categories, // Nama kategori sebagai sumbu x
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: 'Nominal',
                type: 'bar',
                barWidth: '60%',
                data: chartData.values.map((value, index) => ({
                    value: value,
                    itemStyle: {
                        color: chartData.colors[index] // Warna untuk setiap bar
                    }
                }))
            }
        ]
    };

    // Render grafik
    barChart.setOption(barOption);
}

initializeBarChart();


// Doughnut Chart 2 (Revenue Breakdown)
var doughnutChart2 = echarts.init(document.getElementById('doughnutChart2'));
var doughnutOption2 = {
  title: {
    text: 'Revenue Breakdown',
    subtext: 'Product A, B, C',
    left: 'center'
  },
  series: [{
    name: 'Revenue',
    type: 'pie',
    radius: ['40%', '70%'],
    data: [
      {value: 250, name: 'Product A'},
      {value: 100, name: 'Product B'},
      {value: 200, name: 'Product C'}
    ],
    color: ['#28A745', '#FFC107', '#007BFF']
  }]
};
doughnutChart2.setOption(doughnutOption2);

// Doughnut Chart 3 (Revenue Breakdown)
var doughnutChart3 = echarts.init(document.getElementById('doughnutChart3'));
var doughnutOption3 = {
  title: {
    text: 'Revenue Breakdown',
    subtext: 'Product A, B, C',
    left: 'center'
  },
  series: [{
    name: 'Revenue',
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
          fontSize: 40,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
    data: [
      {value: 300, name: 'Product A'},
      {value: 150, name: 'Product B'},
      {value: 100, name: 'Product C'}
    ],
    color: ['#007BFF', '#28A745', '#FFC107']
  }]
};

doughnutChart3.setOption(doughnutOption3);


// Doughnut Chart 4 (Revenue Breakdown)
var doughnutChart4 = echarts.init(document.getElementById('doughnutChart4'));
var doughnutOption4 = {
  title: {
    text: 'Revenue Breakdown',
    subtext: 'Product A, B, C',
    left: 'center'
  },
  series: [{
    name: 'Revenue',
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
          fontSize: 40,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
    data: [
      {value: 300, name: 'Product A'},
      {value: 150, name: 'Product B'},
      {value: 100, name: 'Product C'}
    ],
    color: ['#007BFF', '#28A745', '#FFC107']
  }]
};
doughnutChart4.setOption(doughnutOption4);


// Doughnut Chart 5 (Revenue Breakdown)
var doughnutChart5 = echarts.init(document.getElementById('doughnutChart5'));
var doughnutOption5 = {

  legend: {
    top: '5%',
    left: 'center'
  },
  series: [{
    name: 'Revenue',
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
        fontSize: 40,
        fontWeight: 'bold'
    }
    },
    labelLine: {
    show: false
    },
    data: [
      {value: 300, name: 'Product A'},
      {value: 150, name: 'Product B'},
      {value: 100, name: 'Product C'}
    ],
    color: ['#007BFF', '#28A745', '#FFC107']
  }]
};

doughnutChart5.setOption(doughnutOption5);

// Menambahkan event listener untuk resize
window.addEventListener('resize', function() {
    lineChart.resize();
    doughnutChart1.resize();
    doughnutChart2.resize();
    barChart.resize();
  });
  