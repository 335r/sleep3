import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

#streamlit run E:\Git\网页\答题\答题.py

# 设置页面
st.set_page_config(
    page_title="大学生毕业去向选择分析工具",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
    <style>
    .main {
        background-color: #f5f9ff;
    }
    .stButton>button {
        background-color: #4a86e8;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stRadio>div>div {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .stProgress>div>div>div>div {
        background-color: #4a86e8;
    }
    .result-card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .direction-card {
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
        transition: transform 0.3s;
    }
    .direction-card:hover {
        transform: translateY(-5px);
    }
    </style>
""", unsafe_allow_html=True)

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 职业方向数据（增强版）
directions = {
    "就业": {
        "desc": "直接进入职场，积累工作经验，获得稳定的职业发展",
        "skills": ["专业知识", "沟通能力", "团队合作", "职业素养", "执行力", "行业认知"],
        "careers": ["工程师", "分析师", "市场营销", "项目经理", "人力资源", "产品经理"],
        "color": "#4e79a7",
        "pros": ["稳定收入", "明确晋升路径", "积累行业经验"],
        "cons": ["初期薪资较低", "职业发展可能受限"]
    },
    "升学": {
        "desc": "继续深造，提升学术水平，为未来的职业发展打下坚实基础",
        "skills": ["学术研究", "论文写作", "数据分析", "实验设计", "批判性思维", "专业知识深度"],
        "careers": ["硕士研究生", "博士研究生", "高校教师", "研究员", "科技企业研发", "政策分析"],
        "color": "#f28e2c",
        "pros": ["提升学历竞争力", "深入专业领域", "学术人脉积累"],
        "cons": ["时间成本高", "经济压力可能较大"]
    },
    "出国": {
        "desc": "到国外学习和生活，拓宽国际视野，提升跨文化交流能力",
        "skills": ["外语能力", "跨文化沟通", "适应能力", "国际视野", "独立生活", "全球思维"],
        "careers": ["海外留学生", "国际组织", "跨国公司", "海外学者", "外交领域", "国际商务"],
        "color": "#e15759",
        "pros": ["国际认可学历", "文化体验", "语言能力提升"],
        "cons": ["费用较高", "文化适应挑战"]
    },
    "创业": {
        "desc": "创办自己的企业，实现商业价值和个人梦想",
        "skills": ["创新思维", "资源整合", "商业规划", "领导力", "风险承受", "市场洞察"],
        "careers": ["创始人", "CEO", "创业顾问", "业务总监", "自由职业", "社会企业"],
        "color": "#59a14f",
        "pros": ["实现自我价值", "收入潜力大", "工作自主性强"],
        "cons": ["风险较高", "工作压力大"]
    }
}

# 增强版问题设计（15个问题）
questions = [
    # 学术倾向
    {
        "question": "1. 你对学术研究的兴趣如何？",
        "options": {
            "非常感兴趣，喜欢深入钻研": "升学",
            "比较感兴趣，但更注重实践": "就业",
            "希望通过学术途径出国深造": "出国",
            "更关注实际商业应用": "创业"
        }
    },
    {
        "question": "2. 你的学习成绩在班级中处于？",
        "options": {
            "前10%，有保研可能": "升学",
            "中等偏上，可以考虑考研": "就业",
            "成绩优秀，想申请国外名校": "出国",
            "成绩一般但实践能力强": "创业"
        }
    },

    # 职业倾向
    {
        "question": "3. 你理想的职业发展速度是？",
        "options": {
            "稳步晋升，循序渐进": "就业",
            "先深造再快速成长": "升学",
            "在国际环境中快速发展": "出国",
            "快速实现财务自由": "创业"
        }
    },
    {
        "question": "4. 你对工作稳定性的看法是？",
        "options": {
            "非常重要，希望有保障": "就业",
            "可以接受短期不稳定": "升学",
            "愿意为国际机会冒险": "出国",
            "不看重稳定性": "创业"
        }
    },

    # 个人特质
    {
        "question": "5. 你的性格更接近？",
        "options": {
            "稳重务实": "就业",
            "严谨细致": "升学",
            "开放包容": "出国",
            "冒险创新": "创业"
        }
    },
    {
        "question": "6. 面对挑战时，你通常？",
        "options": {
            "按部就班解决": "就业",
            "深入研究后解决": "升学",
            "寻求国际资源": "出国",
            "寻找创新方案": "创业"
        }
    },

    # 经济因素
    {
        "question": "7. 你的经济状况允许你？",
        "options": {
            "毕业后直接工作": "就业",
            "支持2-3年深造": "升学",
            "承担留学费用": "出国",
            "承担创业风险": "创业"
        }
    },
    {
        "question": "8. 你对初期收入的期望是？",
        "options": {
            "中等即可，看重长期发展": "就业",
            "可以接受较低收入": "升学",
            "希望较高起薪": "出国",
            "不在意初期收入": "创业"
        }
    },

    # 技能评估
    {
        "question": "9. 你的外语水平如何？",
        "options": {
            "可以满足工作需要": "就业",
            "能阅读外文文献": "升学",
            "流利沟通无障碍": "出国",
            "够用就行": "创业"
        }
    },
    {
        "question": "10. 你的实践经历更偏向？",
        "options": {
            "企业实习": "就业",
            "科研项目": "升学",
            "国际交流": "出国",
            "商业实践": "创业"
        }
    },

    # 价值观
    {
        "question": "11. 你最看重工作的？",
        "options": {
            "稳定性": "就业",
            "专业性": "升学",
            "国际性": "出国",
            "自主性": "创业"
        }
    },
    {
        "question": "12. 你的人生目标是？",
        "options": {
            "成为行业专家": "就业",
            "取得学术成就": "升学",
            "体验多元文化": "出国",
            "创造商业价值": "创业"
        }
    },

    # 风险偏好
    {
        "question": "13. 你的风险承受能力？",
        "options": {
            "偏好低风险": "就业",
            "中等风险": "升学",
            "能承受较高风险": "出国",
            "高风险高回报": "创业"
        }
    },
    {
        "question": "14. 面对不确定性，你会？",
        "options": {
            "选择确定路径": "就业",
            "深入研究再做决定": "升学",
            "愿意尝试新环境": "出国",
            "主动创造机会": "创业"
        }
    },

    # 综合评估
    {
        "question": "15. 你希望毕业3年后的生活是？",
        "options": {
            "在企业担任重要职位": "就业",
            "在知名学府深造": "升学",
            "在国外工作学习": "出国",
            "经营自己的事业": "创业"
        }
    }
]

# 初始化session_state
if 'answers' not in st.session_state:
    st.session_state.answers = [None] * len(questions)
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# 主标题
st.title("🎓 大学生毕业去向选择分析（增强版）")
st.markdown("通过15个维度的问题评估，精准分析最适合你的毕业去向")

# 进度条
progress = st.progress((st.session_state.current_question) / len(questions))


# 问题导航（增强版）
def navigate_questions():
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("◀ 上一题"):
                st.session_state.current_question -= 1
                st.rerun()
    with col2:
        if st.session_state.current_question < len(questions) - 1:
            if st.button("下一题 ▶", key="next"):
                if st.session_state.answers[st.session_state.current_question] is None:
                    st.warning("请先选择当前问题的答案")
                else:
                    st.session_state.current_question += 1
                    st.rerun()
        else:
            if st.button("✅ 提交分析", key="submit"):
                if None in st.session_state.answers:
                    st.warning("请完成所有问题后再提交")
                else:
                    st.session_state.submitted = True
                    st.rerun()
    with col3:
        st.caption(f"进度：{st.session_state.current_question + 1}/{len(questions)}")


# 显示当前问题（增强版）
def display_question():
    idx = st.session_state.current_question
    q = questions[idx]

    # 问题卡片
    st.markdown(f"""
        <div style='background-color: white; border-radius: 15px; padding: 25px; 
                    margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1)'>
            <h3>{q['question']}</h3>
        </div>
    """, unsafe_allow_html=True)

    # 显示选项（带图标）
    options = list(q['options'].keys())
    icons = ["🔹", "🔸", "🔻", "🔺"]

    selected = st.radio(
        "请选择最符合你的选项：",
        options,
        index=options.index(st.session_state.answers[idx]) if st.session_state.answers[idx] else 0,
        key=f"question_{idx}",
        format_func=lambda x: f"{icons[options.index(x)]} {x}"
    )

    st.session_state.answers[idx] = selected
    navigate_questions()


# 计算分析结果（增强版）
def calculate_results():
    results = {d: 0 for d in directions.keys()}
    dimension_scores = {d: [] for d in directions.keys()}  # 记录各维度得分

    for i, q in enumerate(questions):
        selected = st.session_state.answers[i]
        if selected:
            direction = q['options'][selected]
            results[direction] += 1
            dimension_scores[direction].append(i + 1)  # 记录问题编号

    # 转换为百分比
    total = sum(results.values())
    for d in results:
        results[d] = round(results[d] / total * 100, 1) if total > 0 else 0

    return results, dimension_scores


# 显示分析结果（增强版）
def display_results():
    st.success("🎉 分析完成！基于15个维度的评估，以下是你的个性化分析报告")

    # 计算得分
    results, dimension_scores = calculate_results()
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    # 主推荐方向
    main_direction = sorted_results[0][0]
    direction_info = directions[main_direction]

    # 结果卡片（增强版）
    st.markdown(f"""
        <div class='result-card'>
            <div style='display: flex; align-items: center; margin-bottom: 20px;'>
                <h2 style='color: {direction_info['color']}; margin: 0;'>你的最佳毕业去向: {main_direction}</h2>
                <span style='margin-left: auto; background-color: {direction_info['color']}; 
                            color: white; padding: 5px 15px; border-radius: 20px;'>
                    匹配度: {results[main_direction]}%
                </span>
            </div>
            <p style='font-size: 18px;'>{direction_info['desc']}</p>

            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;'>
                <div>
                    <h3>🌟 优势领域</h3>
                    <p>你在以下问题上表现出强烈倾向：</p>
                    <ul>
                        {''.join([f'<li>问题{num}</li>' for num in dimension_scores[main_direction][:3]])}
                    </ul>
                </div>
                <div>
                    <h3>📊 方向特点</h3>
                    <p><strong>核心能力：</strong> {', '.join(direction_info['skills'][:4])}...</p>
                    <p><strong>典型职业：</strong> {', '.join(direction_info['careers'][:3])}等</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 详细分析
    with st.expander("📈 查看详细分析结果", expanded=True):
        # 雷达图展示多维评估
        st.subheader("多维能力评估")

        # 准备雷达图数据
        categories = ['学术能力', '职业倾向', '个人特质', '经济因素', '风险偏好']
        values = [
            results["升学"] * 0.8 + results["就业"] * 0.2,
            results["就业"] * 0.7 + results["创业"] * 0.3,
            (results["就业"] + results["出国"] + results["创业"]) / 3,
            results["就业"] * 0.5 + results["升学"] * 0.3 + results["出国"] * 0.2,
            results["创业"] * 0.6 + results["出国"] * 0.4
        ]
        values = [v * 1.2 for v in values]  # 调整比例

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color=direction_info['color'], alpha=0.25)
        ax.plot(angles, values, color=direction_info['color'], linewidth=2)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_title("你的能力维度雷达图", pad=20)
        st.pyplot(fig)

        # 各方向详细对比
        st.subheader("各方向匹配度对比")
        col1, col2 = st.columns([3, 2])

        with col1:
            # 柱状图
            plt.figure(figsize=(10, 6))
            labels = [item[0] for item in sorted_results]
            values = [item[1] for item in sorted_results]
            colors = [directions[label]['color'] for label in labels]

            bars = plt.bar(labels, values, color=colors)
            plt.ylabel('匹配度 (%)')
            plt.ylim(0, 100)

            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{height}%', ha='center', va='bottom')

            st.pyplot(plt)

        with col2:
            # 方向优劣分析
            st.markdown("### 各方向优劣比较")
            for direction, score in sorted_results:
                info = directions[direction]
                st.markdown(f"""
                    <div class='direction-card' style='border-left: 5px solid {info["color"]};'>
                        <div style='display: flex; justify-content: space-between;'>
                            <h4 style='color: {info["color"]}; margin: 0;'>{direction}</h4>
                            <span style='color: {info["color"]}; font-weight: bold;'>{score}%</span>
                        </div>
                        <p><strong>优势：</strong> {', '.join(info['pros'])}</p>
                        <p><strong>挑战：</strong> {', '.join(info['cons'])}</p>
                    </div>
                """, unsafe_allow_html=True)

    # 个性化建议
    st.subheader("📌 个性化发展建议")
    tab1, tab2, tab3 = st.tabs(["短期规划", "中期准备", "长期发展"])

    with tab1:
        st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4>未来6个月建议：</h4>
                <ul>
                    <li>参加3-5场{main_direction}相关的讲座或行业分享会</li>
                    <li>建立{main_direction}领域的人脉网络</li>
                    <li>开始准备{main_direction}所需的核心技能</li>
                    {f'<li>{"收集目标院校信息" if main_direction == "升学" else "筛选目标企业" if main_direction == "就业" else "研究目标国家要求" if main_direction == "出国" else "构思商业计划"}'}</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4>1-2年规划建议：</h4>
                <ul>
                    {f'<li>{"备考研究生/联系导师" if main_direction == "升学" else "积累实习经验" if main_direction == "就业" else "准备语言考试" if main_direction == "出国" else "验证商业模式"}'}</li>
                    <li>提升{direction_info['skills'][0]}和{direction_info['skills'][1]}能力</li>
                    <li>完成2-3个{main_direction}相关的项目</li>
                    <li>参加行业认证考试或培训</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4>3-5年发展建议：</h4>
                <ul>
                    {f'<li>{"在专业领域建立学术影响力" if main_direction == "升学" else "成为部门骨干/管理者" if main_direction == "就业" else "建立国际职业网络" if main_direction == "出国" else "实现企业稳定运营"}'}</li>
                    <li>持续提升{direction_info['skills'][2]}能力</li>
                    <li>建立个人品牌和行业影响力</li>
                    <li>保持学习新兴技术和行业趋势</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    # 重新测试按钮
    st.markdown("---")
    if st.button("🔄 重新测试"):
        st.session_state.answers = [None] * len(questions)
        st.session_state.current_question = 0
        st.session_state.submitted = False
        st.rerun()


# 主程序逻辑
if not st.session_state.submitted:
    display_question()
    progress.progress((st.session_state.current_question + 1) / len(questions))
else:
    display_results()

# 页脚
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
        <p>© 大学生毕业去向分析工具 | 基于15维专业评估 | 数据和分析结果仅供参考</p>
    </div>
""", unsafe_allow_html=True)