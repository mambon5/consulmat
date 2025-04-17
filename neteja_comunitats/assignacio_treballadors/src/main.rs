/*
* Filosofia general:
* Bucle:
*   Mentre faltin comunitats per assignar:
*       Afegim un treballador (amb un itinerari)
*           Mentre el treballador tingui hores per completar (en un dia? En una setmana?)
*           INTENTEM afegir-li comunitats a netejar.
*           TODO: 1) Quina comunitat afegim al treballador que estiguem considerant?
*                 2) Com la inserim a l'itinerari del treballador en consideració?
*                 3) Com decidim si cal netejar l'escala (E) o el vestíbul (V)?
*/

// Per veure la documentació només cal fer
// cargo doc --open

use std::fs;
use std::error::Error;
use std::collections::{HashMap,BTreeSet};

/// Nombre màxim de minuts que un treballador pot treballar en un dia (7h30m)
const MAX_MINUTS_DIA: u32 = 450;
/// Nombre màxim de minuts que un treballador pot treballar en una setmana (40h)
const MAX_MINUTS_SETMANA: u32 = 2400;

/// Un Treballador es modela amb un conjunt de parelles d'itinerari i minuts ocupats, un per a cada
/// dia de la setmana. El dissabte hi és opcionalment.
#[derive(Debug,Clone)]
struct Treballador {
    /// Per a cada dia de la setmana tenim un itinerari
    feiners: [(Vec<usize>, u32); 5],
    /// Dissabte pot contenir (o no) un itinerari
    dissabte: Option<(Vec<usize>, u32)>,
}

impl Treballador {
    /// Constructor
    fn nou() -> Self {
        Self {
            feiners: [(vec![], 0), (vec![], 0), (vec![], 0), (vec![], 0), (vec![], 0)],
            dissabte: None,
        }
    }

    /// Llegeix els minuts ocupats en cada dia de la setmana
    fn llegeix_minuts(&self) -> [u32; 6] {
        let diss = match self.dissabte {
            Some((_, m)) => m,
            None => 0,
        };
        [ self.feiners[0].1, self.feiners[1].1, self.feiners[2].1, self.feiners[3].1, self.feiners[4].1, diss ]
    }

    /// Valida que aquest [`Treballador`] mai fa més hores que [`MAX_MINUTS_DIA`] en cada dia de la setmana, i
    /// que tampoc fa més que [`MAX_MINUTS_SETMANA`] en total
    /// Retorna `true` si les condicions són certes, `false` altrament
    fn valida(&self) -> bool {
        let mins = self.llegeix_minuts();
        (mins.iter().all(|&m| m <= MAX_MINUTS_DIA)) && (mins.iter().sum::<u32>() <= MAX_MINUTS_SETMANA)
    }
}

/// Estructura auxiliar per llegir, desar i consultar una matriu de distàncies
#[derive(Clone,Debug)]
struct Triangular {
    interior: Vec<Vec<u32>>,
}

impl Triangular {
    /// Llegeix la matriu a partir d'un fitxer tipus `.csv`.
    /// El format ha de ser el d'un conjunt de files, on cada fila és una successió de números
    /// separats per comes.
    /// Aquesta funció únicament llegirà el triangle inferior de la matriu, per estalviar espai
    ///
    /// # Errors
    ///
    /// Aquesta funció pot retornar un [`std::io::Error`] en cridar [`std::fs::read_to_string`] o
    /// un [`std::str::FromStr::Err`] en cridar [`str::parse`].
    fn llegeix_matriu(filepath: &str) -> Result<Self, Box<dyn Error>> {
        let continguts = fs::read_to_string(filepath)?;
        let mut interior = vec![];
        for (i, line) in continguts.lines().enumerate() {
            let mut fila = vec![];
            for (_, snum) in line.split(',').enumerate().take_while(|&(j, _)| j < i) {
                let num: u32 = snum.parse()?;
                fila.push(num);
            }
            interior.push(fila);
        }
        Ok(Self{ interior })
    }

    /// Llegeix la distància entre les comunitats `com1` i `com2` a la matriu de distàncies.
    /// Si `com1 == com2`, llavors retorna `0` sense llegir.
    /// Altrament, ordena els índexos per llegir la distància
    ///
    /// # Panic
    ///
    /// Aquesta funció dóna un panic si `com1` o `com2` se surten del rang d'índexos de la matriu

    fn dist(&self, com1: usize, com2: usize) -> u32 {
        if com1 >= self.interior.len() {
            panic!("L'índex {com1} es troba fora del rang de la matriu, que és {}", self.interior.len());
        }
        if com2 >= self.interior.len() {
            panic!("L'índex {com2} es troba fora del rang de la matriu, que és {}", self.interior.len());
        }
        if com1 == com2 {
            0
        } else if com1 < com2 {
            self.interior[com2][com1]
        } else {
            self.interior[com1][com2]
        }
    }
}

//TODO: Quina estructura hauria de guardar totes les comunitats?

/// Comunitat de veïns
#[derive(Clone,Debug)]
struct Comunitat {
    /// Id (en la implementació actual és el número de línia, segons com surten als fitxers de
    /// `Es_i_Vs.txt` i `Comunidades_coords.csv`)
    id: usize,
    /// Dies en els quals visitarem aquesta comunitat (0 = 'Dilluns', 1 = 'Dimarts', ...)
    dies: BTreeSet<usize>,
    /// Nombre de cops que s'ha de netejar el vestíbul (del fitxer `Es_i_Vs.txt`)
    Vs: u8,
    /// Nombre de cops que s'ha de netejar l'escala (del fitxer `Es_i_Vs.txt`)
    Es: u8,
}

impl Comunitat {
    /// Afegeix el dia `dia` a la comunitat
    fn afegeix_dia(&mut self, dia: usize) {
        self.dies.insert(dia);
    }
}

impl From<usize> for Comunitat {
    fn from(id: usize) -> Self {
        Self{ id, dies: BTreeSet::new(), Vs: 0, Es: 0, }
    }
}

/// Llegeix un clúster de comunitats.
/// El format del clúster ha de ser de l'estil de
///
/// > Dilluns: {num},{num}(,...)  
/// > Dimarts: {num},{num}(,...)  
/// > Dimecres: {num},{num}(,...)  
/// > Dijous: {num},{num}(,...)  
/// > Divendres: {num},{num}(,...)  
/// > (opcionalment) Dissabte: {num},{num}(,...)
///
/// # Retorna
/// Aquesta funció retorna un [`std::collections::HashMap`], un diccionari indexat segons l'ID de
/// les comunitats que retorna les pròpies comunitats
///
/// # Errors
///
/// La funció retorna un error si alguna línia no comença amb un dia de la setmana, si no es pot
/// parsejar algun id de comunitat, o si falta algun dia entre dilluns o divendres
fn llegeix_cluster(cluster: &str) -> Result<HashMap<usize, Comunitat>, &'static str> {
    let mut diccionari: HashMap<usize, Comunitat> = HashMap::new();
    let mut dies = [false; 6];
    for line in cluster.lines() {
        let (cap, cua) = line.split_once(": ").unwrap();
        let dia = match cap {
            "Dilluns" => 0,
            "Dimarts" => 1,
            "Dimecres" => 2,
            "Dijous" => 3,
            "Divendres" => 4,
            "Dissabte" => 5,
            _ => {
                return Err("La línia hauria de començar amb algun dia de la setmana");
            },
        };
        dies[dia] = true;
        cua.split(',').map(|sn| sn.parse().unwrap()).for_each(|id| {
            diccionari.entry(id).or_insert(id.into()).afegeix_dia(dia);
        });
    }
    if !dies[..5].into_iter().all(|&d| d) {
        return Err("Falta un dia de la setmana al clúster");
    }
    Ok(diccionari)
}

/// Llegeix les Es i Vs del fitxer `Es_i_Vs.txt`
///
/// # Error
///
/// Aquesta funció pot retornar un [`std::io::Error`] en cridar [`std::fs::read_to_string`]
/// o un [`std::str::FromStr::Err`] en cridar [`str::parse`] sobre els continguts del fitxer.
/// També retornarà error si hi ha comunitats al fitxer `Es_i_Vs.txt` que no es trobin al
/// diccionari de comunitats
fn llegeix_es_i_vs(filepath: &str, comunitats: &mut HashMap<usize, Comunitat>) -> Result<(), Box<dyn Error>> {
    let es_i_vs = fs::read_to_string(filepath)?;
    for (n, line) in es_i_vs.lines().enumerate() {
        let (es,vs) = line.split_once(char::is_whitespace).unwrap();
        let vs = vs.trim_start();
        let es = es.parse()?;
        let vs = vs.parse()?;
        //let mut com = comunitats.get_mut(&n).ok_or(format!("Falta la comunitat amb índex {n}"))?;
        if let Some(com) = comunitats.get_mut(&n) {
            com.Es = es;
            com.Vs = vs;
        }
    }
    Ok(())
}

fn main() -> Result<(), Box<dyn Error>> {
    // Llegim les comunitats
    let resultat_part1 = fs::read_to_string("../src/assig_coms_en_dies/dies_assignats.txt")?;
    let mut comunitats = llegeix_cluster(&resultat_part1)?;
    llegeix_es_i_vs("../input/Es_i_Vs.txt", &mut comunitats)?;
    // Legim les distàncies
    let distancies_peu = Triangular::llegeix_matriu("../output/MatriuDPeu_2025-03-15.csv")?;
    let distancies_cotxe = Triangular::llegeix_matriu("../output/MatriuDCotxe_2025-03-15.csv")?;

    Ok(())
}
