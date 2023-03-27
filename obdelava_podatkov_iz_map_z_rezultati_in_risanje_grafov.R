library(tidyverse)
library(ggplot2)
library(dplyr)
library(rvest)
library(stringr)
library(purrr)

# funkcija, ki nam prebere csv detoteko
preberi_detoteko <- function(ime_detoteke){
  read_csv(ime_detoteke, show_col_types = FALSE, col_names = NULL)
}

# funkcija, ki nam uredi podatke
uredi_podatke <- function(vstavimo, ime_stolpca){
  vstavimo %>%
    mutate(
      povprecje = apply(vstavimo[,3:12],1,mean),
      varianca = round(apply(vstavimo[,3:12],1,var),4)
    ) %>%
    setNames(c("stevilo_zunanjih_tock", "stevilo_notranjih_tock", "čas 1", "čas 2", "čas 3", "čas 4", "čas 5", "čas 6", "čas 7", "čas 8", "čas 9", "čas 10","povprecje","varianca")) %>%
    as.data.frame() %>%
    mutate(
      podatki = ime_stolpca
    ) 
}

#===============================================================================
# NAKLJUČNI KONVEKSNI POLIGON
#===============================================================================

# uredimo podatke za primer, ko imamo za podatke podan naključno generirani konveksni poligon z n zunanjimi in k 
# notranjimi tockami, izračunamo povprečje desetih časov izvajanja algoritma za posamezen par parametrov

tabela <- preberi_detoteko("rezultati.csv")
casi_random_konveksni_poligon <- uredi_podatke(tabela, "poligon")

graf_casov_random_konveksnega_poligona <- ggplot(casi_random_konveksni_poligon, aes(x= casi_random_konveksni_poligon[,2], y = casi_random_konveksni_poligon[,13]))+ 
  aes(color = interaction(casi_random_konveksni_poligon[,1]))+
  scale_color_discrete(name = "število zunanjih točk")+
  geom_line()+
  geom_point()+
  ylim(0,122) +
  labs(x = "število notranjih točk", y = "čas (sekunde)")
graf_casov_random_konveksnega_poligona
ggsave("C:\\Users\\10\\Desktop\\FAKS\\3. letnik\\FINANCNI PRAKTIKUM\\PROJEKT\\TSP-in-the-plane-with-few-interior-points\\KODA\\cas_izvajanja_algoritma_za_nakljucno_generiran_konveksni_poligon.pdf",graf_casov_random_konveksnega_poligona)

poligon_30 <- casi_random_konveksni_poligon[31:45,c(2,13,14,15)]

write.table(poligon_30,"C:\\Users\\10\\Desktop\\FAKS\\3. letnik\\FINANCNI PRAKTIKUM\\PROJEKT\\TSP-in-the-plane-with-few-interior-points\\KODA\\poligon_30.txt", sep = ";" )
#===============================================================================
# PRAVILNI N-KOTNIK
#===============================================================================

tabela1 <- preberi_detoteko("rezultati1.csv")
tabela1[44,7] <- 47
pravilni_n_kotnik <- uredi_podatke(tabela1,"veckotnik")


graf_casov_pravilnega_n_kotnika <- ggplot(pravilni_n_kotnik, aes(x= pravilni_n_kotnik[,2], y = pravilni_n_kotnik[,13]))+ 
  aes(color = interaction(pravilni_n_kotnik[,1]))+
  scale_color_discrete(name = "število zunanjih točk")+
  geom_line()+
  geom_point()+
  ylim(0,122) +
  labs(x = "število notranjih točk", y = "čas (sekunde)")
graf_casov_pravilnega_n_kotnika

ggsave("C:\\Users\\10\\Desktop\\FAKS\\3. letnik\\FINANCNI PRAKTIKUM\\PROJEKT\\TSP-in-the-plane-with-few-interior-points\\KODA\\cas_izvajanja_algoritma_za_pravilni_n_kotnik.pdf",graf_casov_pravilnega_n_kotnika)

n_kotnik_30 <- pravilni_n_kotnik[31:45,c(2,13,14,15)]
write.table(n_kotnik_30,"C:\\Users\\10\\Desktop\\FAKS\\3. letnik\\FINANCNI PRAKTIKUM\\PROJEKT\\TSP-in-the-plane-with-few-interior-points\\KODA\\n_kotnik_30.txt", sep = ";" )


#===============================================================================
# KROŽNICA
#===============================================================================

tabela2 <- preberi_detoteko("rezultati2.csv")
kroznica <- uredi_podatke(tabela2,"kroznica")

graf_casov_kroznice <- ggplot(kroznica, aes(x= kroznica[,2], y = kroznica[,13]))+ 
  aes(color = interaction(kroznica[,1]))+
  scale_color_discrete(name = "število zunanjih točk")+
  geom_line()+
  geom_point()+
  ylim(0,122) +
  labs(x = "število notranjih točk", y = "čas (sekunde)")
graf_casov_kroznice

ggsave("C:\\Users\\10\\Desktop\\FAKS\\3. letnik\\FINANCNI PRAKTIKUM\\PROJEKT\\TSP-in-the-plane-with-few-interior-points\\KODA\\cas_izvajanja_algoritma_za_nakljucne_tocke_na_kroznici.pdf",graf_casov_kroznice)

kroznica_30 <- kroznica[31:45,c(2,13,14,15)]
write.table(kroznica_30,"C:\\Users\\10\\Desktop\\FAKS\\3. letnik\\FINANCNI PRAKTIKUM\\PROJEKT\\TSP-in-the-plane-with-few-interior-points\\KODA\\kroznica_30.txt", sep = ";" )

