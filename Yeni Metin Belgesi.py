import streamlit as st

def hesapla(yas, kilo, boy, cinsiyet, aktiflik):
    # LBM
    if cinsiyet == 'erkek':
        LBM = 0.407 * kilo + 0.267 * boy - 19.2
    else:
        LBM = 0.252 * kilo + 0.473 * boy - 48.3

    # BMI
    BMI = kilo / ((boy / 100) ** 2)
    yagorani = ((kilo - LBM) / kilo) * 100

    # BMI Yorumu
    if BMI <= 18.4:
        bmi_yorum = "Kilonuz ideal aralığın altında. Kilo almanız gerekli."
    elif 18.4 < BMI <= 24.9:
        bmi_yorum = "Kilonuz sağlıklı seviyede."
    elif 25 < BMI <= 29.9:
        bmi_yorum = "Kilonuz biraz yüksek. Yağ oranınızı dikkate alın."
    elif 30 < BMI <= 34.9:
        bmi_yorum = "Obezite başlangıcı. Kilo vermelisiniz."
    elif 35 < BMI <= 39.9:
        bmi_yorum = "Yüksek obezite tehlikesi. Kilo vermelisiniz."
    else:
        bmi_yorum = "Ciddi obezite problemi. Profesyonel yardım alın."

    # Yağ oranı yorumu
    if cinsiyet == "erkek":
        if yagorani < 5:
            yag_yorum = "Yağ oranınız çok düşük."
        elif 5 <= yagorani <= 13:
            yag_yorum = "Atletik yağ oranı."
        elif 13 < yagorani < 17:
            yag_yorum = "Fit seviyede."
        elif 17 <= yagorani <= 24:
            yag_yorum = "Normal vatandaş seviyesi."
        else:
            yag_yorum = "Yüksek yağ oranı."
    else:
        if yagorani < 13:
            yag_yorum = "Yağ oranınız çok düşük."
        elif 13 <= yagorani <= 20:
            yag_yorum = "Atletik yağ oranı."
        elif 21 < yagorani <= 24:
            yag_yorum = "Fit seviyede."
        elif 25 <= yagorani < 31:
            yag_yorum = "Normal vatandaş seviyesi."
        else:
            yag_yorum = "Yüksek yağ oranı."

    # Protein ihtiyacı
    protein_almamin = int(LBM * 1.5)
    protein_almax = int(LBM * 2)
    protein_vermin = int(LBM * 2)
    protein_vermax = int(LBM * 3)

    # BMR
    if cinsiyet == "erkek":
        BMR = (10 * kilo) + (6.25 * boy) - (5 * yas) + 5
    else:
        BMR = (10 * kilo) + (6.25 * boy) - (5 * yas) - 161

    aktiflik_carpani = [1.2, 1.375, 1.55, 1.725, 1.9]
    kcal = BMR * aktiflik_carpani[aktiflik - 1]

    return {
        "LBM": LBM,
        "BMI": BMI,
        "BMI_Yorum": bmi_yorum,
        "Yag_Orani": yagorani,
        "Yag_Yorum": yag_yorum,
        "Protein_Al": (protein_almamin, protein_almax),
        "Protein_Ver": (protein_vermin, protein_vermax),
        "Kalori": kcal
    }

st.title("Vücut Analiz Hesaplayıcı")

yas = st.number_input("Yaşınız (15-99):", min_value=15, max_value=99, value=25)
kilo = st.number_input("Kilonuz (kg):", min_value=1.0, value=70.0)
boy = st.number_input("Boyunuz (cm):", min_value=120, max_value=250, value=170)
cinsiyet = st.selectbox("Cinsiyet:", ["erkek", "kadın"])
aktiflik = st.selectbox("Aktiflik Seviyesi:", [
    "1 - Hareketsiz (yatak başı)",
    "2 - Hafif aktif (az egzersiz)",
    "3 - Orta aktif (haftada 3–5 gün spor)",
    "4 - Çok aktif (yoğun spor)",
    "5 - Aşırı aktif (çift antrenman vs.)"
])

if st.button("HESAPLA"):
    sonuc = hesapla(yas, kilo, boy, cinsiyet, int(aktiflik[0]))
    st.subheader("Sonuçlar")
    st.markdown(f"""
    **LBM:** {sonuc['LBM']:.2f} kg  
    **BMI:** {sonuc['BMI']:.2f} - {sonuc['BMI_Yorum']}  
    **Yağ Oranı:** %{sonuc['Yag_Orani']:.2f} - {sonuc['Yag_Yorum']}  

    **Günlük Protein İhtiyacı:**  
    Kilo Alırken: {sonuc['Protein_Al'][0]}g - {sonuc['Protein_Al'][1]}g  
    Kilo Verirken: {sonuc['Protein_Ver'][0]}g - {sonuc['Protein_Ver'][1]}g  

    **Günlük Kalori İhtiyacı:**  
    Bakım: {sonuc['Kalori']:.0f} kcal  
    Kilo Almak İçin: {sonuc['Kalori']+500:.0f} kcal  
    Kilo Vermek İçin: {sonuc['Kalori']-500:.0f} kcal
    """)
