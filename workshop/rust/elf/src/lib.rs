use std::{
    fmt::Display,
    path::{Path, PathBuf},
};

pub struct CommandLineConfig {
    pub parts: Vec<i32>,
    pub input_path: PathBuf,
}

impl CommandLineConfig {
    pub fn from_args(args: &[&str]) -> Self {
        let mut maybe_part: Option<&str> = None;
        let mut maybe_input: Option<&str> = None;

        for window in args.windows(2) {
            match *window {
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

pub fn read_file_rows<P>(path: P) -> Vec<String>
where
    P: AsRef<Path>,
{
    std::fs::read_to_string(&path)
        .expect("Unable to read file")
        .lines()
        .map(String::from)
        .collect()
}

pub fn print_solution<T>(part: i32, solution: T) -> ()
where
    T: Display,
{
    println!("Part {} solution: {}", part, solution);
}
