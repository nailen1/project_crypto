def plot_msci_style(series, title="Price Chart", ylabel="Price"):
    """
    MSCI 스타일로 시계열 데이터를 플롯하는 함수
    """
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    # MSCI 스타일 설정
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(15, 8))
    fig.patch.set_facecolor('white')
    
    # MSCI 색상 팔레트
    msci_blue = '#003366'
    msci_gray = '#666666'
    msci_light_gray = '#E5E5E5'
    
    # 데이터 플롯
    ax.plot(series.index, series.values, 
            linewidth=2, color=msci_blue, alpha=0.9)
    
    # 제목 및 라벨
    ax.set_title(title, fontsize=18, fontweight='bold', color=msci_blue, pad=25)
    ax.set_xlabel('Time', fontsize=13, fontweight='bold', color=msci_gray)
    ax.set_ylabel(ylabel, fontsize=13, fontweight='bold', color=msci_gray)
    
    # 시간 포맷팅
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))
    
    # Y축 포맷팅
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # 그리드 및 스타일링
    ax.grid(True, color=msci_light_gray, linestyle='-', linewidth=0.5, alpha=0.7)
    ax.set_facecolor('white')
    
    # 축 스타일링
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(msci_gray)
    ax.spines['bottom'].set_color(msci_gray)
    ax.tick_params(colors=msci_gray, which='both')
    
    # 현재 가격 및 통계 계산
    current_price = series.iloc[-1]
    min_price = series.min()
    max_price = series.max()
    price_change = current_price - series.iloc[0]
    price_change_pct = (price_change / series.iloc[0]) * 100
    
    # 현재 가격 라인 (레전드 없이)
    ax.axhline(y=current_price, color='#CC0000', linestyle='--', alpha=0.8, linewidth=1.5)
    
    # 현재 가격 라벨을 라인 근처에 직접 배치
    # X축의 끝 부분(최신 시간)에 현재 가격 라벨 추가
    last_time = series.index[-1]
    ax.annotate(f'${current_price:,.2f}', 
                xy=(last_time, current_price), 
                xytext=(10, 0),  # 라벨을 오른쪽으로 10포인트 이동
                textcoords='offset points',
                fontsize=10, fontweight='bold', color='#CC0000',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor='#CC0000', alpha=0.9),
                arrowprops=dict(arrowstyle='->', color='#CC0000', alpha=0.7))
    
    # 통계 정보 (Current 제외하고 다른 정보만)
    stats_text = f'Open: ${series.iloc[0]:,.2f}\n' \
                f'High: ${max_price:,.2f}\n' \
                f'Low: ${min_price:,.2f}\n' \
                f'Change: ${price_change:+,.2f} ({price_change_pct:+.2f}%)'
    
    # 통계 박스를 좌측 상단에 위치
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='left', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                    edgecolor=msci_light_gray, alpha=0.9))    

    plt.xticks(rotation=45, color=msci_gray)
    plt.tight_layout()
    plt.show()
    
    return fig, ax