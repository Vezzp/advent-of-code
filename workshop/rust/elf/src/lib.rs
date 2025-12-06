use std::{
    fmt::Display,
    path::{Path, PathBuf},
};

pub struct CommandLineConfig {
    pub parts: Vec<i32>,
    pub input_path: PathBuf,
}

impl CommandLineConfig {
    pub fn from_args<A: AsRef<str>>(args: &[A]) -> Self {
        let mut maybe_part: Option<&str> = None;
        let mut maybe_input: Option<&str> = None;

        for window in args.windows(2) {
            let [key, val] = window else { unreachable!() };
            match [key.as_ref(), val.as_ref()] {
                ["-p", part] => maybe_part = Some(part),
                ["-i", input] => maybe_input = Some(input),
                _ => (),
            }
        }

        Self {
            parts: match maybe_part {
                None => vec![1, 2],
                Some(part) => vec![part.parse().expect("Unable to parse part")],
            },
            input_path: maybe_input.unwrap_or("input.txt").into(),
        }
    }
}

pub fn read_file_lines<P: AsRef<Path>>(path: P) -> Vec<String> {
    std::fs::read_to_string(&path)
        .expect("Unable to read file")
        .lines()
        .map(String::from)
        .collect()
}

pub fn print_solution<T: Display>(part: i32, solution: T) -> () {
    println!("Part {} solution: {}", part, solution);
}
