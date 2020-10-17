import time
import sys
import click

from src.cipher_file import *


@click.group()
def main():
    pass


@main.command('e')
@click.option('-k', '--key', type=click.Path(exists=True), required=True,
              help='RSA public key file path')
@click.option('-in', '--in_file', type=click.Path(exists=True), required=True, help='Input file path')
@click.option('-out', '--out_file', type=click.Path(), help='Output file path')
def enc_file(key, in_file, out_file):
    """Encrypt file"""
    try:
        t0 = time.time()
        encrypt_file(get_abs_path(key), get_abs_path(in_file), get_abs_path(out_file))
    except Exception as e:
        click.echo(click.style(str(e), fg='red', bold=True))
    finally:
        t1 = time.time()
        elapsed_time = t1 - t0
        click.echo(click.style(f"Done in: {elapsed_time:0.3f} seconds", fg='blue', bold=True))


@main.command('d')
@click.option('-k', '--key', type=click.Path(exists=True), required=True, help='RSA private key file path')
@click.option('-in', '--in_file', type=click.Path(exists=True), required=True, help='Input file path')
@click.option('-out', '--out_file', type=click.Path(), help='Output file path')
def enc_file(key, in_file, out_file):
    """Decrypt file"""
    try:
        t0 = time.time()
        decrypt_file(get_abs_path(key), get_abs_path(in_file), get_abs_path(out_file))
    except Exception as e:
        click.echo(click.style(str(e), fg='red', bold=True))
    finally:
        t1 = time.time()
        elapsed_time = t1 - t0
        click.echo(click.style(f"Done in: {elapsed_time:0.3f} seconds", fg='blue', bold=True))


@main.command('rsa')
@click.option('-out', '--out_dir', type=click.Path(), help='Output directory')
def rsa_keypair(out_dir):
    """Generate RSA keypair"""
    try:
        t0 = time.time()
        out_dir = out_dir if out_dir else get_curr_dir()
        gen_rsa_keypair(out_dir)
    except Exception as e:
        click.echo(click.style(str(e), fg='red', bold=True))
    finally:
        t1 = time.time()
        elapsed_time = t1 - t0
        click.echo(click.style(f"Done in: {elapsed_time:0.3f} seconds", fg='blue', bold=True))


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        click.echo("Cipher RSA CLI")
    main()
