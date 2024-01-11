
// 通信协议分布
(function() {
    // 1. 实例化对象
    var myChart = echarts.init(document.querySelector(".pie .chart"));

    // 2. 指定配置
    var option = {
      color: ['#485c74', '#bccbb0', '#d8caaf', '#dfd7d7', '#b5c4b1'],
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        bottom: '5%',
        // 图标
        // itemWidth: 10,
        // itemHeight: 10,
        data: ['HTTP', 'HTTPS'],
        // textStyle: {
        //   fontSize: "10"
        // }
      },
      series: [
        {
          name: '通信协议',
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
            { value: 20, name: 'HTTP' },
            { value: 30, name: 'HTTPS' }
          ]
        }
      ]
      };
      
    // 3. 配置实例对象
    myChart.setOption(option);
})();

// 心跳周期分布
(function() {
  // 1. 实例化对象
  var myChart = echarts.init(document.querySelector(".scatter .chart"));

  // 2. 指定配置
  option = {
    color: ['#485c74', '#bccbb0', '#d8caaf', '#dfd7d7', '#b5c4b1'],
    legend: {
      data: ['HTTP', 'HTTPS'],
      bottom: '1%'
    },
    xAxis: {
      name: 'sleeptime',
      nameGap: '30',
      nameLocation: 'center',
      splitLine: false
    },
    yAxis: {
      name: 'frequency',
      nameGap: '30',
      nameLocation: 'center',
      splitLine: false
    },
    series: [
      {
        name: 'HTTP',
        symbolSize: 10,
        data: [
          [10.0, 1],
          [60, 2],
          [100, 2]
        ],
        type: 'scatter'
      },
      {
        name: 'HTTPS',
        symbolSize: 10,
        data: [
          [100, 1],
          [10, 1],
          [100, 3]
        ],
        color: 'green',
        type: 'scatter'
      }
    ]
  };
    
  // 3. 配置实例对象
  myChart.setOption(option);
})();
