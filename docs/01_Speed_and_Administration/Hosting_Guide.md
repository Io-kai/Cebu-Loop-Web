# Hosting & Domain Guide

**Domain Registrar**: Porkbun
**Hosting**: GitHub Pages
**Repo**: `Cebu-Loop-Web`

---

## 1. Domain Configuration (Porkbun)

1. **Login** to Porkbun account.
2. Navigate to **Domain Management** for `cebuloop.com` (or selected domain).
3. **DNS Records**:
    * **Type**: A
    * **Host**: @
    * **Answer**: 185.199.108.153 (GitHub Pages IP 1)
    * **Type**: A
    * **Host**: @
    * **Answer**: 185.199.109.153 (GitHub Pages IP 2)
    * **Type**: CNAME
    * **Host**: www
    * **Answer**: io-kai.github.io (Your GitHub username handle)

## 2. GitHub Pages Setup

1. Go to the Repository **Settings**.
2. Click **Pages** (on the left sidebar).
3. **Source**: Deploy from a branch.
4. **Branch**: `main` (or `master`) / root.
5. **Custom Domain**: Enter `cebuloop.com`.
6. **Enforce HTTPS**: Check this box.

## 3. Updates

* Pushing changes to the `main` branch will automatically update the live site.
* Allow 1-2 minutes for propagation.

## 4. Email (Google Workspace)

* In Porkbun DNS, ensure **MX Records** are set for Google Workspace.
* Usually, Porkbun has a "Quick Connect" feature for Google Workspace. Use that to auto-populate MX records.
